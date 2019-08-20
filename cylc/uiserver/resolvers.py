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

"""GraphQL resolvers for use in data accessing and mutation of workflows."""

from cylc.flow.network.resolvers import (
    workflow_filter, node_filter, sort_elements
)
from cylc.flow.ws_data_mgr import ID_DELIM


class Resolvers(object):

    def __init__(self, ws_mgr, data_mgr):
        self.ws_mgr = ws_mgr
        self.data_mgr = data_mgr

    # Query resolvers
    # workflows
    async def get_workflow_msgs(self, args):
        """Return list of workflows."""
        return sort_elements(
            [flow_msg
             for flow_msg in self.data_mgr.data.values()
             if workflow_filter(flow_msg, args)],
            args)

    # nodes
    async def get_nodes_all(self, node_type, args):
        """Return nodes from all workflows, filter by args."""
        return sort_elements(
            [n
             for k in await self.get_workflow_msgs(args)
             for n in getattr(k, node_type)
             if node_filter(n, args)],
            args)

    async def get_nodes_by_ids(self, node_type, args):
        """Return protobuf node objects for given id."""
        nat_ids = set(args.get('native_ids', []))
        w_ids = set()
        for nat_id in nat_ids:
            o_name, w_name, _ = nat_id.split(ID_DELIM, 2)
            w_ids.add(f'{o_name}{ID_DELIM}{w_name}')
        if node_type == 'proxy_nodes':
            nodes = (
                n
                for w_id in w_ids
                for n in (
                    list(getattr(
                            self.data_mgr.data[w_id],
                            'task_proxies', []))
                    + list(getattr(
                            self.data_mgr.data[w_id],
                            'family_proxies', []))))
        else:
            nodes = (
                n
                for w_id in w_ids
                for n in getattr(self.data_mgr.data[w_id], node_type, []))
        return sort_elements(
            [node
             for node in nodes
             if node.id in nat_ids and node_filter(node, args)],
            args)

    async def get_node_by_id(self, node_type, args):
        """Return protobuf node object for given id."""
        n_id = args.get('id')
        o_name, w_name, _ = n_id.split(ID_DELIM, 2)
        w_id = f'{o_name}{ID_DELIM}{w_name}'
        flow_msg = self.data_mgr.data[w_id]
        if node_type == 'proxy_nodes':
            nodes = (
                list(getattr(flow_msg, 'task_proxies', []))
                + list(getattr(flow_msg, 'family_proxies', [])))
        else:
            nodes = getattr(flow_msg, node_type, [])
        for node in nodes:
            if node.id == n_id:
                return node
        return None

    # edges
    async def get_edges_all(self, args):
        """Return edges from all workflows, filter by args."""
        return sort_elements(
            [e
             for w in await self.get_workflow_msgs(args)
             for e in getattr(w, 'edges')],
            args)

    async def get_edges_by_ids(self, args):
        """Return protobuf edge objects for given id."""
        nat_ids = set(args.get('native_ids', []))
        w_ids = set()
        for nat_id in nat_ids:
            oname, wname, eid = nat_id.split(ID_DELIM, 2)
            w_ids.add(f'{oname}{ID_DELIM}{wname}')
        return sort_elements(
            [e
             for f in w_ids
             for e in getattr(self.data_mgr.data[f], 'edges')],
            args)

    # Mutations
    async def mutator(self, info, command, w_args, args):
        """Mutate workflow."""
        w_ids = [
            flow.workflow.id
            for flow in await self.get_workflow_msgs(w_args)]
        # Pass the request to the workflow GraphQL endpoints
        req_str, variables, _, _ = info.context.get('graphql_params')
        graphql_args = {
            'request_string': req_str,
            'variables': variables,
        }
        return self.ws_mgr.multi_request('graphql', w_ids, graphql_args)

    async def nodes_mutator(self, info, command, ids, w_args, args):
        """Mutate node items of associated workflows."""
        w_ids = set([
            flow.workflow.id
            for flow in await self.get_workflow_msgs(w_args)])
        if not w_ids:
            return 'Error: No matching Workflow'
        # Pass the multi-node request to the workflow GraphQL endpoints
        req_str, variables, _, _ = info.context.get('graphql_params')
        graphql_args = {
            'request_string': req_str,
            'variables': variables,
        }
        multi_args = {w_id: graphql_args for w_id in w_ids}
        return self.ws_mgr.multi_request(
            'graphql', w_ids, multi_args=multi_args)
