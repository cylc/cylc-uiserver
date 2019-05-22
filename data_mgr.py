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
from fnmatch import fnmatchcase

# from google.protobuf.json_format import MessageToDict

from cylc.exceptions import ClientError, ClientTimeout
from cylc.ws_messages_pb2 import PbEntireWorkflow
from cylc.network.scan import MSG_TIMEOUT


# TODO: define in and import this from cylc-flow
# maps methods in cylc-flow server to the returned bytes message
METHOD_MAP = {
    'pb_entire_workflow': PbEntireWorkflow
}


async def get_workflow_data(w_id, client, method):
    # Use already established client
    try:
        pb_msg = await client.async_request(method)
    except ClientTimeout as exc:
        return (w_id, MSG_TIMEOUT)
    except ClientError as exc:
        return (w_id, None)
    else:
        ws_data = METHOD_MAP[method]()
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
        new_data = {}
        ws_args = (
            (w_id, info['req_client'], 'pb_entire_workflow')
            for w_id, info in self.ws_mgr.workflows.items())
        gathers = ()
        for args in ws_args:
            if not ids or args[0] in ids:
                gathers += (get_workflow_data(*args),)
        items = await asyncio.gather(*gathers)
        for w_id, result in items:
            if result is not None and result != MSG_TIMEOUT:
                new_data[w_id] = result
        if not ids:
            # atomic update
            self.data = new_data
        else:
            self.data.update(new_data)

    # Data access filters
    def get_workflow_msgs(self, args):
        """Return list of workflows."""
        result = []
        for flow_msg in self.data.values():
            if self._workflow_filter(flow_msg, args):
                result.append(flow_msg)
        # TODO: Sorting and Pagination
        return result

    def get_nodes_all(self, node_type, args):
        """Return nodes from all workflows, filter by args."""
        w_args = {
            'ids': args['workflows'],
            'exids': args['exworkflows'],
        }
        nodes = [
            n for k in self.get_workflow_msgs(w_args)
            for n in getattr(k, node_type)]
        result = []
        for node in nodes:
            if self._node_filter(node, args):
                result.append(node)
        # TODO: Sorting and Pagination
        return result

    def get_nodes_by_id(self, node_type, args):
        """Return protobuf node objects for given id."""
        nat_ids = args.get('native_ids', [])
        w_ids = []
        for nat_id in nat_ids:
            o_name, w_name, nid = nat_id.split('/', 2)
            w_ids.append(f"{o_name}/{w_name}")
        if node_type == 'proxy_nodes':
            nodes = (
                n for w_id in set(w_ids)
                for n in (
                    list(getattr(self.data[w_id], 'task_proxies', []))
                    + list(getattr(self.data[w_id], 'family_proxies', []))))
        else:
            nodes = (
                n for w_id in set(w_ids)
                for n in getattr(self.data[w_id], node_type, []))
        result = []
        for node in nodes:
            if ((not nat_ids or node.id in set(nat_ids)) and
                    self._node_filter(node, args)):
                result.append(node)
        # TODO: Sorting and Pagination
        return result

    def get_node_by_id(self, node_type, args):
        """Return protobuf node object for given id."""
        n_id = args.get('id')
        o_name, w_name, remainder = n_id.split('/', 2)
        w_id = f"{o_name}/{w_name}"
        if node_type == 'proxy_nodes':
            nodes = (
                list(getattr(self.data[w_id], 'task_proxies', []))
                + list(getattr(self.data[w_id], 'family_proxies', [])))
        else:
            nodes = getattr(self.data[w_id], node_type, [])
        for node in nodes:
            if node.id == n_id:
                return node
        return None

    def get_edges_all(self, args):
        """Return edges from all workflows, filter by args."""
        w_args = {
            'ids': args['workflows'],
            'exids': args['exworkflows'],
        }
        result = []
        for edge in [
                n for k in self.get_workflow_msgs(w_args)
                for n in getattr(k, 'edges')]:
            result.append(edge)
        # TODO: Sorting and Pagination
        return result

    def get_edges_by_id(self, args):
        """Return protobuf edge objects for given id."""
        nat_ids = args.get('native_ids', [])
        w_ids = []
        for nat_id in nat_ids:
            oname, wname, eid = nat_id.split('/', 2)
            w_ids.append(f"{oname}/{wname}")
        w_ids = list(set(w_ids))
        result = []
        for edge in [
                e for k in w_ids
                for e in getattr(self.data[k], 'edges')]:
            result.append(edge)
        # TODO: Sorting and Pagination
        return result

    def _node_filter(self, node, args):
        """Filter nodes based on attribute arguments"""
        natts = self._collate_node_atts(node)
        return (
                (not args.get('states') or node.state in args['states']) and
                not (args.get('exstates') and
                     node.state in args['exstates']) and
                (args.get('mindepth', -1) < 0 or
                    node.depth >= args['mindepth']) and
                (args.get('maxdepth', -1) < 0 or
                    node.depth <= args['maxdepth']) and
                (not args.get('ids') or
                    self._node_atts_filter(natts, args['ids'])) and
                not (args.get('exids') and
                     self._node_atts_filter(natts, args['exids'])))

    def _workflow_filter(self, flow, args):
        """Filter workflows based on attribute arguments"""
        natts = [flow.workflow.owner, flow.workflow.name, flow.workflow.status]
        return (
                (not args.get('ids') or
                    self._workflow_atts_filter(natts, args['ids'])) and
                not (args.get('exids') and
                     self._workflow_atts_filter(natts, args['exids'])))

    @staticmethod
    def _workflow_atts_filter(natts, items):
        """Match components of id argument with those of workflow id."""
        for owner, name, status in set(items):
            if ((not owner or fnmatchcase(natts[0], owner)) and
                    (not name or fnmatchcase(natts[1], name)) and
                    (not status or natts[2] == status)):
                return True
        return False

    @staticmethod
    def _node_atts_filter(natts, items):
        """Match node id argument with node attributes."""
        for owner, workflow, cycle, name, submit_num, state in items:
            if ((not owner or fnmatchcase(natts[0], owner)) and
                    (not workflow or fnmatchcase(natts[1], workflow)) and
                    (not cycle or fnmatchcase(natts[2], cycle)) and
                    any(fnmatchcase(nn, name) for nn in natts[3]) and
                    (not submit_num or
                        fnmatchcase(str(natts[4]), submit_num.lstrip('0'))) and
                    (not state or natts[5] == state)):
                return True
        return False

    @staticmethod
    def _collate_node_atts(node):
        """Collate node filter attributes."""
        node_id = getattr(node, 'id')
        slash_count = node_id.count('/')
        n_id = node_id.split('/', slash_count)
        if slash_count == 2:
            n_cycle = None
            n_name = n_id[2]
        else:
            n_cycle = n_id[2]
            n_name = n_id[3]
        return [
            n_id[0],
            n_id[1],
            n_cycle,
            getattr(node, 'namespace', [n_name]),
            getattr(node, 'submit_num', None),
            getattr(node, 'state', None),
        ]
