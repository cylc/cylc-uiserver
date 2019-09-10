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

from cylc.flow.network.resolvers import BaseResolvers
from cylc.flow.ws_data_mgr import WORKFLOW


class Resolvers(BaseResolvers):
    """UI Server context GraphQL query and mutation resolvers."""

    ws_mgr = None

    def __init__(self, data, **kwargs):
        super().__init__(data)

        # Set extra attributes
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)

    # Mutations
    async def mutator(self, info, *m_args):
        """Mutate workflow."""
        _, w_args, _ = m_args
        w_ids = [
            flow[WORKFLOW].id
            for flow in await self.get_workflows_data(w_args)]
        # Pass the request to the workflow GraphQL endpoints
        req_str, variables, _, _ = info.context.get('graphql_params')
        graphql_args = {
            'request_string': req_str,
            'variables': variables,
        }
        return self.ws_mgr.multi_request('graphql', w_ids, graphql_args)

    async def nodes_mutator(self, info, *m_args):
        """Mutate node items of associated workflows."""
        _, _, w_args, _ = m_args
        w_ids = [
            flow[WORKFLOW].id
            for flow in await self.get_workflows_data(w_args)]
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
