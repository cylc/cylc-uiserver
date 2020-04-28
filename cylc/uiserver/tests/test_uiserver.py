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

from cylc.uiserver.main import *
from tornado.web import StaticFileHandler, RequestHandler
from cylc.uiserver.handlers import TornadoGraphQLHandler


def test_my_application():
    """Test creating the Tornado app."""
    my_application = MyApplication(handlers=[])
    assert not my_application.is_closing
    my_application.signal_handler(None, None)
    assert my_application.is_closing


def test_cylcuiserver_absolute_path():
    """Test a Cylc UI server created with absolute path for static assets."""
    cylc_uiserver = CylcUIServer(8000, '/static/path', '/users/test')
    assert cylc_uiserver._port == 8000
    assert cylc_uiserver._static == '/static/path'
    assert cylc_uiserver._jupyter_hub_service_prefix == '/users/test'


def test_cylcuiserver_relative_path():
    """Test a Cylc UI server created with relative path for static assets."""
    cylc_uiserver = CylcUIServer(8000, './', '/users/test')
    assert cylc_uiserver._port == 8000
    print(cylc_uiserver._static)
    # the code is using the directory relative to the main script ATM
    assert cylc_uiserver._static.endswith('cylc/uiserver')
    assert cylc_uiserver._jupyter_hub_service_prefix == '/users/test'


def test_cylcuiserver_create_static_handler():
    cylc_uiserver = CylcUIServer(8000, './static', '/prefix/')
    handler = cylc_uiserver._create_static_handler('(imgs/*.png)')
    assert "/prefix/((imgs/*.png))" == handler[0]
    assert handler[1] == StaticFileHandler
    assert handler[2].get('path').endswith("/static")


def test_cylcuiserver_create_handler():
    cylc_uiserver = CylcUIServer(8000, './', '/prefix/')
    handler = cylc_uiserver._create_handler('tests', RequestHandler,
                                            schema=True, table=False,
                                            number=1)
    assert "/prefix/tests" == handler[0]
    assert handler[1] == RequestHandler
    assert handler[2].get('schema')
    assert not handler[2].get('table')
    assert handler[2].get('number') == 1


def test_cylcuiserver_create_graphql_handler():
    cylc_uiserver = CylcUIServer(8000, './', '/prefix/')
    handler = cylc_uiserver._create_graphql_handler(
        'tests', TornadoGraphQLHandler, graphiql=True)
    assert "/prefix/tests" == handler[0]
    assert handler[1] == TornadoGraphQLHandler
    assert handler[2].get('schema')
    assert handler[2].get('resolvers')
    assert handler[2].get('graphiql') == 1
