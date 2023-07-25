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
from pathlib import Path
import sys
from typing import (
    TYPE_CHECKING, Any, Dict, Iterable, List, Optional, Union
)

import zmq.asyncio

from cylc.flow.id import Tokens
from cylc.flow.exceptions import ClientError, ClientTimeout
from cylc.flow.network import API
from cylc.flow.network.client import WorkflowRuntimeClient
from cylc.flow.network.scan import (
    api_version,
    contact_info,
    is_active,
    scan,
    validate_contact_info
)
from cylc.flow.workflow_files import (
    ContactFileFields as CFF,
    WorkflowFiles,
)

if TYPE_CHECKING:
    from logging import Logger


CLIENT_TIMEOUT = 2.0


async def workflow_request(
    client: WorkflowRuntimeClient,
    command: str,
    args: Optional[Dict[str, Any]] = None,
    timeout: Optional[float] = None,
    *,
    log: Optional['Logger'] = None,
    req_meta: Optional[Dict[str, Any]] = None
) -> Union[bytes, object]:
    """Workflow request command.

    Args:
        client: Instantiated workflow client.
        command: Command/Endpoint name.
        args: Endpoint arguments.
        timeout: Client request timeout (secs).
        req_meta: Meta data related to request, e.g. auth_user
    """
    try:
        return await client.async_request(
            command, args, timeout, req_meta=req_meta
        )
    except (ClientTimeout, ClientError) as exc:
        # Expected error
        if log:
            log.error(f"{type(exc).__name__}: {exc}")
        else:
            print(exc, file=sys.stderr)
        exc.workflow = client.workflow
        raise exc
    except Exception as exc:
        # Unexpected error
        msg = f"Error communicating with {client.workflow}"
        if log:
            log.error(msg)
            log.exception(exc)
        else:
            print(msg, file=sys.stderr)
            print(exc, file=sys.stderr)
        raise exc


async def run_coros_in_order(*coros):
    """Run the provided coroutines in order."""
    for coro in coros:
        await coro


def db_file_exists(flow) -> bool:
    """Return True if the workflow database exists."""
    return Path(
        flow['path'],
        WorkflowFiles.Service.DIRNAME,
        WorkflowFiles.Service.DB
    ).exists()


class WorkflowsManager:  # noqa: SIM119
    """Object for tracking workflows by performing filesystem scans.

    * Detects stopped & running workflows in the run dir.
    * Registers/connects/disconnects/unregisters workflows with the data store.

    """

    def __init__(self, uiserver, log, context=None, run_dir=None) -> None:
        self.uiserver = uiserver
        self.log = log
        if context is None:
            self.context = zmq.asyncio.Context()
        else:
            self.context = context
        self.owner = getuser()

        # all workflows currently tracked
        self.workflows: 'Dict[str, Dict]' = {}

        # the "workflow pipe" used to detect workflows on the filesystem
        self._scan_pipe = (
            # all flows on the filesystem
            scan(run_dir)
            # stop here is the flow is stopped, else...
            | is_active(is_active=True, filter_stop=False)
            # extract info from the contact file
            | contact_info
            # ensure required contact file fields are present
            | validate_contact_info
            # only flows which are using the same api version
            | api_version(f'=={API}')
        )

        # queue for requesting new scans, valid queued values are:
        # * True  - (stop=True)  The stop signal (stops the scanner)
        # * False - (stop=False) Request a new scan
        # * None  - The "stopped" signal, sent after the scan task has stopped
        self._queue: 'asyncio.Queue[Union[bool, None]]' = asyncio.Queue()

        # signal that the scanner is stopping, subsequent scan requests
        # will be ignored
        self._stopping = False

    def get_workflows(self):
        return self.uiserver.data_store_mgr.get_workflows()

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
        active_before, inactive_before = self.get_workflows()

        active = set()
        inactive = set()

        async for flow in self._scan_pipe:
            # where possible yield results within this `async for` loop to
            # allow the data store to get to work whilst we complete the scan
            # (prevents one slow filesystem operation holding up the works)

            # append fields to scan results
            flow['owner'] = self.owner
            wid = Tokens(user=flow['owner'], workflow=flow['name']).id
            flow['id'] = wid

            if not flow.get('contact'):
                # this flow isn't running
                inactive.add(wid)
                if (
                    # if the workflow has previously started...
                    self.workflows.get(wid, {}).get(CFF.UUID)
                    # ...but the database has since been removed...
                    and not db_file_exists(flow)
                ):
                    # ...then it is no longer the same run, the transition is:
                    #   <before-state> => None > <after-state>
                    # so we use a special /<before-state> marker
                    if wid in active_before:
                        yield (wid, '/active', 'inactive', flow)
                    else:
                        yield (wid, '/inactive', 'inactive', flow)

                elif wid in active_before:
                    yield (wid, 'active', 'inactive', flow)
                elif wid in inactive_before:
                    pass
                else:
                    yield (wid, None, 'inactive', flow)

            elif (
                wid in self.workflows
                and flow[CFF.UUID] != self.workflows[wid].get(CFF.UUID)
            ):
                # this flow is running but it's a different run
                active.add(wid)
                if wid in active_before:
                    yield (wid, '/active', 'active', flow)
                else:
                    yield (wid, '/inactive', 'active', flow)

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
        try:
            flow['req_client'] = WorkflowRuntimeClient(flow['name'])
        except ClientError as exc:
            self.log.debug(f'Could not connect to {wid}: {exc}')
            return False
        self.workflows[wid] = flow
        await self.uiserver.data_store_mgr.connect_workflow(
            wid,
            flow
        )
        return True

    async def _disconnect(self, wid):
        """Disconnect from a running workflow.

        Marks the workflow as stopped.
        """
        self.uiserver.data_store_mgr.disconnect_workflow(wid)
        with suppress(KeyError, IOError):
            self.workflows[wid]['req_client'].stop(stop_loop=False)
        with suppress(KeyError):
            self.workflows[wid]['req_client'] = None

    async def _unregister(self, wid):
        """Unregister a workflow from the data store."""
        await self.uiserver.data_store_mgr.unregister_workflow(wid)
        if wid in self.workflows:
            self.workflows.pop(wid)

    async def update(self) -> None:
        """Scans for workflows, handles any state changes.

        Don't call this method directly, call self.scan to queue an update.

        Possible workflow states:
            active:
                (i.e. running, held, stopping)
            inactive:
                (i.e. stopped or registered)
            None:
                (i.e. unregistered)

        Between scans workflows can jump from any state to any other state.

        """
        tasks: List[asyncio.Task] = []

        def run(*coros):
            # start tasks running as soon as possible
            # (we could be connecting to workflows whilst the scan is still
            # running)
            nonlocal tasks
            tasks.append(asyncio.create_task(run_coros_in_order(*coros)))

        # handle state changes
        async for wid, before, after, flow in self._workflow_state_changes():
            if before == 'active':
                if after == 'inactive':
                    # workflow has stopped
                    run(self._disconnect(wid))

                elif after is None:
                    # workflow has stopped and been deleted
                    run(
                        self._disconnect(wid),
                        self._unregister(wid),
                    )

            elif before is None:
                if after == 'active':
                    # workflow has been created and started
                    run(
                        self._register(wid, flow, is_active=True),
                        self._connect(wid, flow),
                    )

                elif after == 'inactive':
                    # workflow has been created
                    run(self._register(wid, flow, is_active=False))

            elif before == 'inactive':
                if after == 'active':
                    # workflow has been started
                    run(self._connect(wid, flow))

                elif after is None:
                    # workflow has been deleted
                    run(self._unregister(wid))

            elif before.startswith('/'):
                # workflow is no longer the same run as before e.g:
                # * db has been removed whilst workflow stopped
                # * run dir has been deleted and re-created
                cmds = []
                if before == '/active':
                    # disconnect from the old workflow
                    cmds.append(self._disconnect(wid))
                # re-register the workflow
                cmds.extend([
                    self._unregister(wid),
                    self._register(wid, flow, is_active=(after == 'active')),
                ])
                if after == 'active':
                    # connect to the new workflow
                    cmds.append(self._connect(wid, flow))
                run(*cmds)

        # wait for everything we have actioned to complete before returning
        await asyncio.gather(*tasks)

    async def multi_request(
        self,
        command: str,
        workflows: Iterable[str],
        args: Optional[Dict[str, Any]] = None,
        multi_args: Optional[Dict[str, Any]] = None,
        timeout=None,
        req_meta: Optional[Dict[str, Any]] = None
    ) -> List[Union[bytes, object, Exception]]:
        """Send requests to multiple workflows."""
        if args is None:
            args = {}
        if multi_args is None:
            multi_args = {}
        if req_meta is None:
            req_meta = {}
        gathers = [
            workflow_request(
                self.workflows[w_id]['req_client'],
                command,
                multi_args.get(w_id, args),
                timeout,
                log=self.log,
                req_meta=req_meta
            )
            for w_id in workflows
            # skip stopped workflows
            if self.workflows.get(w_id, {}).get('req_client')
        ]
        return await asyncio.gather(*gathers, return_exceptions=True)

    async def scan(self):
        """Request a new workflow scan."""
        if not self._stopping and self._queue.empty():
            await self._queue.put(False)

    async def run(self):
        """Coroutine that performs workflow scans on request asynchronously.

        Note:
            Because we do this with a loop rather than with a periodic callback
            scan operations cannot overlap. Important because the data store
            must complete the requested changes before a new scan can begin.

            See https://github.com/cylc/cylc-uiserver/issues/312

        """
        stop = False
        while not stop:
            try:
                await self.update()
            except Exception as exc:
                # log exceptions but carry on
                # (otherwise a temporary issue will kill the scan task)
                self.log.exception(exc)
            try:
                stop = await self._queue.get()  # wait for a signal
            except RuntimeError:
                # RuntimeError may be raised if the event loop is closed
                break
        # inform stop() that this task has completed
        await self._queue.put(None)

    async def stop(self):
        """Stop the workflow scanner task.

        Request the "run" task to stop and wait for confirmation that it has.
        """
        # prevent any new scans being requested
        self._stopping = True
        # wipe any scan requests
        while not self._queue.empty():
            status = await self._queue.get()
            if status is None:
                # the scanner stopped itself i.e. RuntimeError
                return
        # request the scan task to stop
        await self._queue.put(True)
        # wait for confirmation that it has
        # (note the async sleep appears to be necessary otherwise tornado
        # does not recognise that the scan task has completed)
        await asyncio.sleep(0)
        await self._queue.get()
