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

import importlib

import cylc.uiserver.schema
from cylc.uiserver.schema import NODE_MAP as UIS_NODE_MAP


def test_node_map():
    """Check that we have implemented Graphene classes for GraphQL types."""
    cylc_flow_schema = importlib.import_module('cylc.flow.network.schema')
    importlib.reload(cylc_flow_schema)
    NODE_MAP = cylc_flow_schema.NODE_MAP
    uis_type_names = set(UIS_NODE_MAP.keys()).difference(NODE_MAP.keys())
    assert uis_type_names
    for type_name in uis_type_names:
        _class = getattr(cylc.uiserver.schema, type_name)
        # It is not straightforward to check that _class is a Graphene class
        assert 'graphene' in type(_class).__module__
