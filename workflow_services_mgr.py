#!/usr/bin/env python3

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
import sys
import socket

from tornado import gen

from cylc import flags
from cylc.hostuserutil import is_remote_host, get_host_ip_by_name
from cylc.network.client import SuiteRuntimeClient
from cylc.network.scan import (
    get_scan_items_from_fs, re_compile_filters, MSG_TIMEOUT)

CLIENT_TIMEOUT = 2.0


async def est_workflow(reg, host, port, timeout=None):
    """Establish communication with workflow, setting up REQ client."""
    if is_remote_host(host):
        try:
            host = get_host_ip_by_name(host)  # IP reduces DNS traffic
        except socket.error as exc:
            if cylc.flags.debug:
                raise
            sys.stderr.write("ERROR: %s: %s\n" % (exc, host))
            return (reg, host, port, None)

    # NOTE: Connect to the suite by host:port. This way the
    #       SuiteRuntimeClient will not attempt to check the contact file
    #       which would be unnecessary as we have already done so.
    # NOTE: This part of the scan *is* IO blocking.
    client = SuiteRuntimeClient(reg, host=host, port=port, timeout=timeout)

    result = {}
    result['client'] = client
    try:
        msg = await client.async_request('identify')
    except ClientTimeout as exc:
        return (reg, host, port, MSG_TIMEOUT)
    except ClientError as exc:
        return (reg, host, port, result or None)
    else:
        result.update(msg)
    return (reg, host, port, result)


class WorkflowServicesMgr(object):

    def __init__(self):
        self.workflows = {}

    def spawn_workflow(self):
        # TODO - Spawn workflows
        pass

    async def gather_workflows(self):
        workflows = {}
        cre_owner, cre_name = re_compile_filters(None, ['.*'])
        scan_args = (
            (reg, host, port, CLIENT_TIMEOUT)
            for reg, host, port in
            get_scan_items_from_fs(cre_owner, cre_name))

        items = await gen.multi([est_workflow(*x) for x in scan_args])
        for reg, host, port, info in items:
            if info is not None and info != MSG_TIMEOUT:
                owner = info['owner']
                workflows[f"{owner}/{reg}"] = {
                    'name': info['name'],
                    'owner': owner,
                    'host': host,
                    'port': port,
                    'version': info['version'],
                    'req_client': info['client'],
                }
        # atomic update
        self.workflows = workflows
