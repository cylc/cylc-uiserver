# -*- coding: utf-8 -*-
# Copyright (C) 2019 NIWA & British Crown (Met Office) & Contributors.
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
import logging
import socket

import zmq.asyncio

from cylc.flow import flags
from cylc.flow.exceptions import ClientError, ClientTimeout
from cylc.flow.hostuserutil import is_remote_host, get_host_ip_by_name
from cylc.flow.network import API
from cylc.flow.network.client import SuiteRuntimeClient
from cylc.flow.network.scan import (
    get_scan_items_from_fs, re_compile_filters, MSG_TIMEOUT)
from cylc.flow.data_store_mgr import ID_DELIM

from typing import Any, Dict, List, Optional, Set, Tuple, Union

logger = logging.getLogger(__name__)
CLIENT_TIMEOUT = 2.0


async def workflow_request(
        client: Any,
        command: str,
        args: Optional[Dict[str, Any]] = None,
        timeout: Optional[int] = None,
        req_context: Any = None)\
        -> Tuple[Any, Optional[Union[str, Dict[Any, Any]]]]:
    """Workflow request command.

    Args:
        client (object): Instantiated workflow client.
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


async def est_workflow(reg: str, host: str, port: int,
                       pub_port: int, context: Any = None,
                       timeout: Optional[int] = None)\
        -> Tuple[str, str, int, int, Any,
                 Optional[Union[str, Dict[Any, Any]]]]:
    """Establish communication with workflow, instantiating REQ client."""
    if is_remote_host(host):
        try:
            host = get_host_ip_by_name(host)  # IP reduces DNS traffic
        except socket.error as exc:
            if flags.debug:
                raise
            logger.error("ERROR: %s: %s\n", exc, host)
            return (reg, host, port, pub_port, None, None)

    # NOTE: Connect to the suite by host:port. This way the
    #       SuiteRuntimeClient will not attempt to check the contact file
    #       which would be unnecessary as we have already done so.
    # NOTE: This part of the scan *is* IO blocking.
    client = SuiteRuntimeClient(reg, host=host, port=port,
                                context=context, timeout=timeout)
    _, result = await workflow_request(client, 'identify')
    return (reg, host, port, pub_port, client, result)


class WorkflowsManager:
    """Discover and Manage workflows."""

    def __init__(self, uiserver: Any, context: zmq.asyncio.Context = None) \
            -> None:
        self.uiserver = uiserver
        if context is None:
            self.context = zmq.asyncio.Context()
        else:
            self.context = context
        self.workflows: Dict[Any, Any] = {}
        self.stopping: Set[Any] = set()

    def spawn_workflow(self) -> None:
        """Start/spawn a workflow."""
        # TODO - Spawn workflows
        pass

    async def gather_workflows(self) -> None:
        """Scan, establish, and discard workflows."""
        scanflows: Dict[str, Dict[Any, Any]] = {}
        cre_owner, cre_name = re_compile_filters(None, ['.*'])
        scan_args: List[Any] = [
            (reg, host, port, pub_port, self.context, CLIENT_TIMEOUT)
            for reg, host, port, pub_port, api in
            get_scan_items_from_fs(cre_owner, cre_name)
            if reg not in self.stopping and api == str(API)]
        # clear stopping set
        self.stopping.clear()

        gathers: List[Any] = []
        for arg in scan_args:
            gathers.append(est_workflow(*arg))
        items = await asyncio.gather(*gathers)
        for reg, host, port, pub_port, client, info in items:
            if info is not None and info != MSG_TIMEOUT:
                owner = info['owner']
                scanflows[f"{owner}{ID_DELIM}{reg}"] = {
                    'name': info['name'],
                    'owner': owner,
                    'host': host,
                    'port': port,
                    'pub_port': pub_port,
                    'version': info['version'],
                    'req_client': client,
                }

        # Check existing against scan
        for w_id, info in list(self.workflows.items()):
            if w_id in scanflows:
                if (info['host'] == scanflows[w_id]['host'] and
                        info['port'] == scanflows[w_id]['port']):
                    client = scanflows[w_id]['req_client']
                    with suppress(IOError):
                        client.stop(stop_loop=False)
                    scanflows.pop(w_id)
                continue
            client = self.workflows[w_id]['req_client']
            with suppress(IOError):
                client.stop(stop_loop=False)
            self.workflows.pop(w_id)
            self.uiserver.data_store_mgr.purge_workflow(w_id)

        # update with new, and start data sync
        gathers = []
        for w_id, w_info in scanflows.items():
            self.workflows[w_id] = w_info
            gathers.append(
                self.uiserver.data_store_mgr.sync_workflow(
                    w_id, w_info['name'], w_info['host'], w_info['pub_port']
                )
            )
        await asyncio.gather(*gathers)

    async def multi_request(
            self,
            command: str,
            workflows: List[Any],
            args: Optional[Dict[str, Any]] = None,
            multi_args: Optional[Dict[str, Any]] = None,
            timeout: Optional[int] = None) -> List[Any]:
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
        gathers: List[Any] = []
        for info, request_args in req_args.items():
            gathers.append(workflow_request(req_context=info, *request_args))
        results = await asyncio.gather(*gathers)
        res = []
        for _, val in results:
            res.extend([
                msg_core
                for msg_core in list(val.values())[0].get('result')
                if isinstance(val, dict) and list(val.values())])
        return res
