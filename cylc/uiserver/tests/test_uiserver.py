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

import pytest

from graphene_tornado.tornado_graphql_handler import TornadoGraphQLHandler
from tornado.web import RequestHandler

from cylc.uiserver.main import CylcUIServer, MyApplication


def test_my_application():
    """Test creating the Tornado app."""
    my_application = MyApplication(handlers=[])
    assert not my_application.is_closing
    my_application.signal_handler(None, None)
    assert my_application.is_closing


def test_cylcuiserver_create_handler():
    cylc_uiserver = CylcUIServer(8000, '/prefix/')
    handler = cylc_uiserver._create_handler('tests', RequestHandler,
                                            schema=True, table=False,
                                            number=1)
    assert "/prefix/tests" == handler[0]
    assert handler[1] == RequestHandler
    assert handler[2].get('schema')
    assert not handler[2].get('table')
    assert handler[2].get('number') == 1


def test_cylcuiserver_create_graphql_handler():
    cylc_uiserver = CylcUIServer(8000, '/prefix/')
    handler = cylc_uiserver._create_graphql_handler(
        'tests', TornadoGraphQLHandler, graphiql=True)
    assert "/prefix/tests" == handler[0]
    assert handler[1] == TornadoGraphQLHandler
    assert handler[2].get('schema')
    assert handler[2].get('resolvers')
    assert handler[2].get('graphiql') == 1


def test_ui_blank_config(mock_config, ui_build_dir):
    """It should serve the bundled UIS by default."""
    uis = CylcUIServer(8000, '/prefix/')
    assert uis.ui_path.parts[-4:-1] == ('cylc', 'uiserver', 'ui')


def test_ui_version_unset(mock_config, ui_build_dir):
    """It should pick the most recent UI version found."""
    # test with a valid ui_build_path
    mock_config(f'c.UIServer.ui_build_dir="{ui_build_dir}"')
    uis = CylcUIServer(8000, '/prefix/')
    assert uis.ui_path == ui_build_dir / '3.0'

    # test with an invalid ui_build_path
    mock_config('c.UIServer.ui_build_dir="beef"')
    with pytest.raises(Exception):
        uis = CylcUIServer(8000, '/wellington/')
        uis.ui_path  # forces computation of the ui_path


def test_ui_version_specified(mock_config, ui_build_dir):
    """If the UI version is specified it should use that one."""
    # test with an installed version
    mock_config(f'''
        c.UIServer.ui_build_dir="{ui_build_dir}"
        c.UIServer.ui_version="1.0"
    ''')
    uis = CylcUIServer(8000, '/prefix/')
    assert uis.ui_path == ui_build_dir / '1.0'

    # test with an uninstalled version
    mock_config(f'''
        c.UIServer.ui_build_dir="{ui_build_dir}"
        c.UIServer.ui_version="5.0"
    ''')
    with pytest.raises(Exception):
        uis = CylcUIServer(8000, '/prefix/')
        uis.ui_path  # forces computation of the ui_path


def test_ui_build_dir(mock_config, ui_build_dir):
    """If the UI build path does is a UI build it should use it."""
    mock_config(f'''
        c.UIServer.ui_build_dir="{ui_build_dir / '2.0'}"
        # the ui_version should do nothing here
        c.UIServer.ui_version="99"
    ''')
    uis = CylcUIServer(8000, '/prefix/')
    assert uis.ui_path == ui_build_dir / '2.0'


def test_ui_build_dir_argument(mock_config, ui_build_dir):
    """The ui_build_dir argument should override any config value."""
    # config asks for 2.0
    mock_config(f'''
        c.UIServer.ui_build_dir="{ui_build_dir / '2.0'}"
    ''')
    uis = CylcUIServer(8000, '/prefix/')
    # normally this would be used
    assert uis.ui_path == ui_build_dir / '2.0'
    # argument asks for 1.0
    uis = CylcUIServer(8000, '/prefix/', ui_build_dir / '1.0')
    # argument wins
    assert uis.ui_path == ui_build_dir / '1.0'
