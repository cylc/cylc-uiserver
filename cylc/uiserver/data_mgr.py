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

"""Create and update the data structure for all workflow services."""

import asyncio

# from google.protobuf.json_format import MessageToDict

from cylc.flow.exceptions import ClientError, ClientTimeout
from cylc.flow.network.server import PB_METHOD_MAP
from cylc.flow.network.scan import MSG_TIMEOUT


async def get_workflow_data(w_id, client, method):
    # Use already established client
    try:
        pb_msg = await client.async_request(method)
    except ClientTimeout as exc:
        return (w_id, MSG_TIMEOUT)
    except ClientError as exc:
        return (w_id, None)
    else:
        ws_data = PB_METHOD_MAP[method]()
        ws_data.ParseFromString(pb_msg)
    return (w_id, ws_data)


class DataManager(object):

    def __init__(self, ws_mgr):
        self.ws_mgr = ws_mgr
        self.data = {}

    # Data syncing
    async def entire_workflow_update(self, ids=None):
        if ids is None:
            ids = []

        # Prune old data
        for w_id in list(self.data):
            if w_id not in self.ws_mgr.workflows:
                del self.data[w_id]

        # Fetch new data
        ws_args = (
            (w_id, info['req_client'], 'pb_entire_workflow')
            for w_id, info in self.ws_mgr.workflows.items())
        gathers = ()
        for args in ws_args:
            if not ids or args[0] in ids:
                gathers += (get_workflow_data(*args),)
        items = await asyncio.gather(*gathers)
        new_data = {}
        for w_id, result in items:
            if result is not None and result != MSG_TIMEOUT:
                new_data[w_id] = {
                    'edges': {e.id: e for e in result.edges},
                    'families': {f.id: f for f in result.families},
                    'family_proxies': {n.id: n for n in result.family_proxies},
                    'jobs': {j.id: j for j in result.jobs},
                    'tasks': {t.id: t for t in result.tasks},
                    'task_proxies': {n.id: n for n in result.task_proxies},
                    'workflow': result.workflow,
                }

        self.data.update(new_data)
