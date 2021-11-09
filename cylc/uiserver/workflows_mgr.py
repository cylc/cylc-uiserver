# Copyright (C) NIWA & British Crown (Met Office) & Contributors.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""Manage Workflow services.

Includes:
    - Spawning (#TODO)
    - Scans/updates
    - ZeroMQ REQ/RES client initiation and checks
    - ?

"""
import asyncio
from contextlib import suppress
from getpass import getuser
import sys

import zmq.asyncio

from cylc.flow import ID_DELIM
from cylc.flow.exceptions import ClientError, ClientTimeout
from cylc.flow.network import API
from cylc.flow.network.client import WorkflowRuntimeClient
from cylc.flow.network import MSG_TIMEOUT
from cylc.flow.network.scan import (
    api_version,
    contact_info,
    is_active,
    scan
)
from cylc.flow.workflow_files import ContactFileFields as CFF

CLIENT_TIMEOUT = 2.0


async def workflow_request(
    client,
    command,
    args=None,
    timeout=None,
    req_context=None,
    *,
    log=None,
):
    """Workflow request command.

    Args:
        client (WorkflowRuntimeClient): Instantiated workflow client.
        command (str): Command/Endpoint name.
        args (dict): Endpoint arguments.
        timeout (float): Client request timeout (secs).
        req_context (str): A string to identifier.

    Returns:
        tuple: (req_context, result)

    """
    if req_context is None:
        req_context = command
    try:
        result = await client.async_request(command, args, timeout)
        return (req_context, result)
    except ClientTimeout as exc:
        if log:
            log.exception(exc)
        else:
            print(exc, file=sys.stderr)
        return (req_context, MSG_TIMEOUT)
    except ClientError as exc:
        if log:
            log.exception(exc)
        else:
            print(exc, file=sys.stderr)
        return (req_context, None)


class WorkflowsManager:

    def __init__(self, uiserver, log, context=None, run_dir=None):
        self.uiserver = uiserver
        self.log = log
        if context is None:
            self.context = zmq.asyncio.Context()
        else:
            self.context = context
        self.owner = getuser()
        self.active = {}
        self.stopping = set()
        self.inactive = set()
        self._scan_pipe = (
            # all flows on the filesystem
            scan(run_dir)
            # only flows which have a contact file
            # | is_active(True)
            # stop here is the flow is stopped, else...
            | is_active(True, filter_stop=False)
            # extract info from the contact file
            | contact_info
            # only flows which are using the same api version
            | api_version(f'=={API}')
        )

    def spawn_workflow(self):
        """Start/spawn a workflow."""
        # TODO - Spawn workflows
        pass

    async def _workflow_state_changes(self):
        """Scan workflows and yield state change events.

        Yields:
            tuple - (wid, before, after, flow)

            wid (str):
                The workflow ID.
            before (str):
                The state at the last scan ('active', 'inactive', None)
            after (str):
                The state at this scan ('active', 'inactive', None)
            flow (dict):
                The scan data (i.e. the contents of the contact file).

        """
        active_before = set(self.active)
        inactive_before = set(self.inactive)

        active = set()
        inactive = set()

        async for flow in self._scan_pipe:
            flow['owner'] = self.owner
            wid = f'{flow["owner"]}{ID_DELIM}{flow["name"]}'
            flow['id'] = wid

            if not flow.get('contact'):
                # this flow isn't running
                inactive.add(wid)
                if wid in active_before:
                    yield (wid, 'active', 'inactive', flow)
                elif wid in inactive_before:
                    pass
                else:
                    yield (wid, None, 'inactive', flow)

            elif (
                wid in self.active
                and flow[CFF.UUID] != self.active[wid].get(CFF.UUID)
            ):
                # this flow is running but it's a different run
                active.add(wid)
                yield (wid, 'active', 'inactive', self.active[wid])
                yield (wid, 'inactive', 'active', flow)

            else:
                # this flow is running
                active.add(wid)
                if wid in active_before:
                    pass
                elif wid in inactive_before:
                    yield (wid, 'inactive', 'active', flow)
                else:
                    yield (wid, None, 'active', flow)

        for wid in active_before - (active | inactive):
            yield (wid, 'active', None, None)

        for wid in inactive_before - (active | inactive):
            yield (wid, 'inactive', None, None)

    async def _register(self, wid, flow, is_active):
        """Register a new workflow with the data store."""
        await self.uiserver.data_store_mgr.register_workflow(wid, is_active)

    async def _connect(self, wid, flow):
        """Open a connection to a running workflow."""
        self.active[wid] = flow
        flow['req_client'] = WorkflowRuntimeClient(flow['name'])
        await self.uiserver.data_store_mgr.sync_workflow(
            wid,
            flow
        )

    async def _disconnect(self, wid):
        """Disconnect from a running workflow."""
        try:
            client = self.active[wid]['req_client']
        except KeyError:
            pass
        else:
            with suppress(IOError):
                client.stop(stop_loop=False)

    async def _unregister(self, wid):
        """Unregister a workflow from the data store."""
        await self.uiserver.data_store_mgr.unregister_workflow(wid)

    async def _stop(self, wid):
        """Mark a workflow as stopped.

        The workflow can't do this itself, because it's not running.
        """
        self.uiserver.data_store_mgr.stop_workflow(wid)

    async def update(self):
        """Scans for workflows, handles any state changes.

        Possible workflow states:
            active:
                (i.e. running, held, stopping)
            inactive:
                (i.e. stopped or registered)
            None:
                (i.e. unregistered)

        Between scans workflows can jump from any state to any other state.

        """
        self.stopping.clear()

        async for wid, before, after, flow in self._workflow_state_changes():
            # handle state changes
            if before == 'active' and after == 'inactive':
                await self._disconnect(wid)
                await self._stop(wid)

            elif before == 'active' and after is None:
                await self._disconnect(wid)
                await self._unregister(wid)

            elif before is None and after == 'active':
                await self._register(wid, flow, is_active=True)
                await self._connect(wid, flow)

            elif before is None and after == 'inactive':
                await self._register(wid, flow, is_active=False)

            elif before == 'inactive' and after == 'active':
                await self._connect(wid, flow)

            elif before == 'inactive' and after is None:
                await self._unregister(wid)

            # finally update the new states for internal purposes
            if before == 'active':
                self.active.pop(wid)
            elif (
                before == 'inactive'
                and wid in self.inactive
            ):
                self.inactive.remove(wid)
            if after == 'active':
                self.active[wid] = flow
            elif after == 'inactive':
                self.inactive.add(wid)

    async def multi_request(
        self,
        command,
        workflows,
        args=None,
        multi_args=None,
        timeout=None
    ):
        """Send requests to multiple workflows."""
        if args is None:
            args = {}
        if multi_args is None:
            multi_args = {}
        req_args = {
            w_id: (
                self.active[w_id]['req_client'],
                command,
                multi_args.get(w_id, args),
                timeout,
            ) for w_id in workflows
            if w_id in self.active
        }
        gathers = [
            workflow_request(req_context=info, *request_args, log=self.log)
            for info, request_args in req_args.items()
        ]
        results = await asyncio.gather(*gathers, return_exceptions=True)
        res = []
        for result in results:
            if isinstance(result, Exception):
                self.log.exception(
                    'Failed to send requests to multiple workflows',
                    exc_info=result
                )
            else:
                _, val = result
                res.extend([
                    msg_core
                    for msg_core in list(val.values())[0].get('result')
                    if isinstance(val, dict)
                    and list(val.values())
                ])
        return res
