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

from cylc.uiserver.app import CylcUIServer


def test_ui_blank_config():
    """It should serve the bundled UIS by default."""
    uis = CylcUIServer()
    assert uis.ui_path.parts[-4:-1] == ('cylc', 'uiserver', 'ui')


def test_ui_version_unset(mock_config, ui_build_dir):
    """It should pick the most recent UI version found."""
    # test with a valid ui_build_path
    mock_config(CylcUIServer={'ui_build_dir': ui_build_dir})
    uis = CylcUIServer()
    uis.initialize_settings()
    assert uis.ui_path == ui_build_dir / '3.0'

    # test with an invalid ui_build_path
    mock_config(CylcUIServer={'ui_build_dir': 'beef'})
    uis = CylcUIServer()
    with pytest.raises(Exception):
        uis.initialize_settings()
        uis.ui_path  # forces computation of the ui_path


def test_ui_version_specified(mock_config, ui_build_dir):
    """If the UI version is specified it should use that one."""
    # test with an installed version
    mock_config(CylcUIServer={
        'ui_build_dir': ui_build_dir,
        'ui_version': '1.0'
        })
    uis = CylcUIServer()
    uis.initialize_settings()
    assert uis.ui_path == ui_build_dir / '1.0'

    # test with an uninstalled version
    mock_config(CylcUIServer={
        'ui_build_dir': ui_build_dir,
        'ui_version': '5.0'
        })
    uis = CylcUIServer()
    with pytest.raises(Exception):
        uis.initialize_settings()
        uis.ui_path  # forces computation of the ui_path


def test_ui_build_dir(mock_config, ui_build_dir):
    """If the UI build path does is a UI build it should use it."""
    mock_config(CylcUIServer={
        'ui_build_dir': ui_build_dir / '2.0',
        # the ui_version should do nothing here
        'ui_version': '99'
        })
    uis = CylcUIServer()
    uis.initialize_settings()
    assert uis.ui_path == ui_build_dir / '2.0'


# def test_ui_build_dir_argument(mock_config, ui_build_dir):
#     """The ui_build_dir argument should override any config value."""
#     # config asks for 2.0
#     mock_config(CylcUIServer={
#         'ui_build_dir': ui_build_dir / '2.0'
#         })
#     uis = CylcUIServer()
#     uis.initialize_settings()
#     # normally this would be used
#     assert uis.ui_path == ui_build_dir / '2.0'
#     # argument asks for 1.0
#     uis = CylcUIServer(8000, '/prefix/', ui_build_dir / '1.0')
#     uis.initialize_settings()
#     # argument wins
#     assert uis.ui_path == ui_build_dir / '1.0'
