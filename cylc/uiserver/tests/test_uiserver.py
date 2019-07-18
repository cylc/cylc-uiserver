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

import os

from cylc.uiserver.main import *


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
