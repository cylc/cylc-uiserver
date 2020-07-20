# -*- coding: utf-8 -*-
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
import logging
import socket

import zmq.asyncio

from cylc.flow import flags, ID_DELIM
from cylc.flow.exceptions import ClientError, ClientTimeout
from cylc.flow.hostuserutil import is_remote_host, get_host_ip_by_name
from cylc.flow.network import API
from cylc.flow.network.client import SuiteRuntimeClient
from cylc.flow.network.scan import MSG_TIMEOUT
from cylc.flow.network.scan_nt import (
    api_version,
    contact_info,
    is_active,
    scan
)
from cylc.flow.suite_files import ContactFileFields

logger = logging.getLogger(__name__)
CLIENT_TIMEOUT = 2.0


async def workflow_request(client, command, args=None,
                           timeout=None, req_context=None):
    """Workflow request command.

    Args:
        client (SuiteRuntimeClient): Instantiated workflow client.
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
        logger.exception(exc)
        return (req_context, MSG_TIMEOUT)
    except ClientError as exc:
        logger.exception(exc)
        return (req_context, None)


async def est_workflow(reg, host, port, pub_port, context=None, timeout=None):
    """Establish communication with workflow, instantiating REQ client."""
    if is_remote_host(host):
        try:
            host = get_host_ip_by_name(host)  # IP reduces DNS traffic
        except socket.error as exc:
            if flags.debug:
                raise
            logger.error("ERROR: %s: %s\n", exc, host)
            return (reg, host, port, pub_port, None)

    # NOTE: Connect to the suite by host:port. This way the
    #       SuiteRuntimeClient will not attempt to check the contact file
    #       which would be unnecessary as we have already done so.
    # NOTE: This part of the scan *is* IO blocking.
    client = SuiteRuntimeClient(reg, context=context, timeout=timeout)
    _, result = await workflow_request(client, 'identify')
    return (reg, host, port, pub_port, client, result)


class WorkflowsManager:
    """Discover and Manage workflows."""

    def __init__(self, uiserver, context=None):
        self.uiserver = uiserver
        if context is None:
            self.context = zmq.asyncio.Context()
        else:
            self.context = context
        self.workflows = {}
        self.stopping = set()
        self.scan_pipe = (
            # all flows on the filesystem
            scan
            # only flows which have a contact file
            | is_active(True)
            # extract info from the contact file
            | contact_info
            # only flows which are using the same api version
            | api_version(f'=={API}')
        )

    def spawn_workflow(self):
        """Start/spawn a workflow."""
        # TODO - Spawn workflows
        pass

    async def gather_workflows(self):
        """Scan, establish, and discard workflows."""
        self.stopping.clear()

        # keep track of what's changed since the last scan
        before = set(self.workflows)
        after = set()

        # start scanning
        async for flow in self.scan_pipe:
            name = flow['name']
            wid = f'{getuser()}{ID_DELIM}{flow["name"]}'
            after.add(wid)
            present_before = wid in before

            # reshape the data for the uiserver
            flow.update({
                'id': wid,
                # 'name': name,
                'owner': getuser(),
                'host': flow[ContactFileFields.HOST],
                'port': flow[ContactFileFields.PORT],
                'pub_port': flow[ContactFileFields.PUBLISH_PORT],
                'version': flow[ContactFileFields.VERSION],
                'uuid': flow[ContactFileFields.UUID]
            })

            # if this workflow was present before, is it still the same run?
            restarted = False
            if present_before:
                if flow['uuid'] != self.workflows[wid]['uuid']:
                    restarted = True
                    self.workflows.pop(wid)
                    self.uiserver.data_store_mgr.purge_workflow(wid)

            # is it a new run?
            if restarted or not present_before:
                flow['req_client'] = SuiteRuntimeClient(name)
                self.workflows[wid] = flow
                await self.uiserver.data_store_mgr.sync_workflow(
                    wid, name, flow['host'], flow['pub_port']
                )

        # tidy up stopped flows
        for wid in before - after:
            client = self.workflows[wid]['req_client']
            with suppress(IOError):
                client.stop(stop_loop=False)
            self.workflows.pop(wid)
            self.uiserver.data_store_mgr.purge_workflow(wid)

    async def multi_request(self, command, workflows, args=None,
                            multi_args=None, timeout=None):
        """Send requests to multiple workflows."""
        if args is None:
            args = {}
        if multi_args is None:
            multi_args = {}
        req_args = {}
        for w_id in workflows:
            cmd_args = multi_args.get(w_id, args)
            req_args[w_id] = (
                self.workflows[w_id]['req_client'],
                command,
                cmd_args,
                timeout,
            )
        gathers = ()
        for info, request_args in req_args.items():
            gathers += (workflow_request(req_context=info, *request_args),)
        results = await asyncio.gather(*gathers)
        res = []
        for _, val in results:
            res.extend([
                msg_core
                for msg_core in list(val.values())[0].get('result')
                if isinstance(val, dict) and list(val.values())])
        return res
