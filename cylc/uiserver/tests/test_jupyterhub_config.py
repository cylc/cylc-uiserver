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
"""Tests for jupyterhub_config module."""

from cylc.uiserver.jupyterhub_config import check_cylc_site_conf_path
from cylc.uiserver.config_util import CONF_FILE_NAME, SITE_CONF_ROOT


def test_cylc_site_conf_path_ok(tmp_path, caplog):
    """Method passes valid file without comment"""
    (tmp_path / CONF_FILE_NAME).touch()
    assert check_cylc_site_conf_path(tmp_path) == tmp_path
    assert caplog.messages == []


def test_cylc_site_conf_path_unreadable(tmp_path, caplog):
    """Method logs error because file exists but is unreadable."""
    (tmp_path / CONF_FILE_NAME).touch()
    (tmp_path / CONF_FILE_NAME).chmod(0)
    assert check_cylc_site_conf_path(tmp_path) == SITE_CONF_ROOT
    assert caplog.messages[0].startswith('Unable to read config file at')


def test_cylc_site_conf_path_empty(tmp_path, caplog):
    """Method logs error because file does not exist."""
    assert check_cylc_site_conf_path(tmp_path) == tmp_path
    assert 'does not exist' in caplog.messages[0]
