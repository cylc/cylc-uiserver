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

import os
from pathlib import Path

import pytest

from cylc.uiserver import __file__ as UIS_PKG
from cylc.uiserver.config import load


SYS_CONF = Path(UIS_PKG).parent / 'config_defaults.py'
USER_CONF = Path('~/.cylc/hub/config.py').expanduser()
SITE_CONF = Path('/etc/cylc/hub/config.py')


@pytest.fixture
def clear_env(monkeypatch):
    for envvar in ('CYLC_SITE_CONF_PATH',):
        if envvar in os.environ:
            monkeypatch.delenv(envvar)


@pytest.fixture
def capload(monkeypatch):
    """Capture config file load events.

    Prevents the config files from being loaded, equivalent to having
    empty config files.
    """
    files = []
    monkeypatch.setattr('cylc.uiserver.config._load', files.append)
    return files


def test_config(clear_env, capload):
    """It should load the system, site and user configs in that order."""
    load()
    assert capload == [
        SYS_CONF,
        SITE_CONF,
        USER_CONF,
    ]


def test_cylc_site_conf_path(clear_env, capload, monkeypatch):
    """The site config should change to $CYLC_SITE_CONF_PATH if set."""
    monkeypatch.setenv('CYLC_SITE_CONF_PATH', 'elephant')
    load()
    assert capload == [
        SYS_CONF,
        Path('elephant/hub/config.py'),
        USER_CONF,
    ]
