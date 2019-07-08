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

from fnmatch import fnmatchcase
from cylc.flow.network.resolvers import (
    collate_workflow_atts, workflow_atts_filter, workflow_filter,
    collate_node_atts, node_atts_filter, node_filter)


class Resolvers(object):

    def __init__(self, ws_mgr, data_mgr):
        self.ws_mgr = ws_mgr
        self.data_mgr = data_mgr

    # Query resolvers
    # workflows
    async def get_workflow_msgs(self, args):
        """Return list of workflows."""
        return [
            flow_msg for flow_msg in self.data_mgr.data.values()
            if workflow_filter(flow_msg, args)]

    # nodes
    async def get_nodes_all(self, node_type, args):
        """Return nodes from all workflows, filter by args."""
        return [
            n for k in await self.get_workflow_msgs(args)
            for n in getattr(k, node_type)
            if node_filter(n, args)]

    async def get_nodes_by_id(self, node_type, args):
        """Return protobuf node objects for given id."""
        nat_ids = args.get('native_ids', [])
        w_ids = []
        for nat_id in nat_ids:
            o_name, w_name, _ = nat_id.split('/', 2)
            w_ids.append(f'{o_name}/{w_name}')
        if node_type == 'proxy_nodes':
            nodes = (
                n for w_id in set(w_ids) for n in (
                    list(getattr(
                            self.data_mgr.data[w_id],
                            'task_proxies', []))
                    + list(getattr(
                            self.data_mgr.data[w_id],
                            'family_proxies', []))))
        else:
            nodes = (
                n for w_id in set(w_ids) for n in
                getattr(self.data_mgr.data[w_id], node_type, []))
        return [node for node in nodes
                if ((not nat_ids or node.id in set(nat_ids)) and
                    node_filter(node, args))]

    async def get_node_by_id(self, node_type, args):
        """Return protobuf node object for given id."""
        n_id = args.get('id')
        o_name, w_name, _ = n_id.split('/', 2)
        w_id = f'{o_name}/{w_name}'
        if node_type == 'proxy_nodes':
            nodes = (
                list(getattr(
                    self.data_mgr.data[w_id], 'task_proxies', []))
                + list(getattr(
                    self.data_mgr.data[w_id], 'family_proxies', [])))
        else:
            nodes = getattr(self.data_mgr.data[w_id], node_type, [])
        for node in nodes:
            if node.id == n_id:
                return node
        return None

    # edges
    async def get_edges_all(self, args):
        """Return edges from all workflows, filter by args."""
        return [
            e for w in await self.get_workflow_msgs(args)
            for e in getattr(w, 'edges')]

    async def get_edges_by_id(self, args):
        """Return protobuf edge objects for given id."""
        nat_ids = args.get('native_ids', [])
        w_ids = []
        for nat_id in nat_ids:
            oname, wname, eid = nat_id.split('/', 2)
            w_ids.append(f'{oname}/{wname}')
        w_ids = list(set(w_ids))
        return list(
            e for f in w_ids for e in getattr(self.data_mgr.data[f], 'edges'))

    # Mutations
    async def mutator(self, command, w_args, args):
        """Mutate workflow."""
        w_ids = [flow.workflow.id
                 for flow in await self.get_workflow_msgs(w_args)]
        return self.ws_mgr.multi_request(command, w_ids, args)

    async def nodes_mutator(self, command, ids, w_args, args):
        """Mutate node items of associated workflows."""
        w_ids = [flow.workflow.id
                 for flow in await self.get_workflow_msgs(w_args)]
        if not w_ids:
            return 'Error: No matching Workflow'
        # match proxy ID args with workflows
        flow_ids = []
        multi_args = {}
        for w_id in w_ids:
            items = []
            for owner, workflow, cycle, name, submit_num, state in ids:
                if workflow and owner is None:
                    owner = "*"
                if (not (owner and workflow) or
                        fnmatchcase(w_id, f'{owner}/{workflow}')):
                    if cycle is None:
                        cycle = '*'
                    id_arg = f'{cycle}/{name}'
                    if submit_num:
                        id_arg = f'{id_arg}/{submit_num}'
                    if state:
                        id_arg = f'{id_arg}:{state}'
                    items.append(id_arg)
            if items:
                flow_ids.append(w_id)
                multi_args[w_id] = args
                if command == 'insert_tasks':
                    multi_args[w_id]['items'] = items
                elif command == 'put_messages':
                    multi_args[w_id]['task_job'] = items[0]
                else:
                    multi_args[w_id]['task_globs'] = items
        return self.ws_mgr.multi_request(
            command, flow_ids, multi_args=multi_args)
