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
from cylc.uiserver import config_util

import pytest

from cylc.flow.cfgspec.globalcfg import GlobalConfig
from cylc.uiserver import __file__ as UIS_PKG
from cylc.uiserver.config_util import (
    UISERVER_DIR,
    get_conf_dir_hierarchy,
)
from cylc.uiserver.jupyterhub_config import load


SYS_CONF = Path(UIS_PKG).parent / 'jupyter_config.py'
USER_CONF = Path('~/.cylc/uiserver').expanduser()
SITE_CONF = Path('/etc/cylc/uiserver')


@pytest.fixture
def clear_env(monkeypatch: pytest.MonkeyPatch):
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
    monkeypatch.setattr('cylc.uiserver.jupyterhub_config._load', files.append)
    return files


def test_config(clear_env, capload: list, monkeypatch: pytest.MonkeyPatch):
    """It should load the system, site and user configs in that order."""
    monkeypatch.setattr(config_util, '__version__', '0')
    # This constant was set before clear_env took effect:
    monkeypatch.setattr(
        'cylc.uiserver.jupyterhub_config.SITE_CONF_ROOT',
        Path(GlobalConfig.DEFAULT_SITE_CONF_PATH, UISERVER_DIR)
    )
    load()
    assert capload == [
        SYS_CONF,
        (SITE_CONF / 'jupyter_config.py'),
        (SITE_CONF / '0/jupyter_config.py'),
        (USER_CONF / 'jupyter_config.py'),
        (USER_CONF / '0/jupyter_config.py')
    ]


def test_cylc_site_conf_path(clear_env, capload, monkeypatch):
    """The site config should change to $CYLC_SITE_CONF_PATH if set."""
    monkeypatch.setenv('CYLC_SITE_CONF_PATH', 'elephant')
    monkeypatch.setattr(config_util, '__version__', '0')
    load()
    assert capload == [
        SYS_CONF,
        Path('elephant/uiserver/jupyter_config.py'),
        Path('elephant/uiserver/0/jupyter_config.py'),
        Path(USER_CONF / 'jupyter_config.py'),
        Path(USER_CONF / '0/jupyter_config.py')
    ]


def test_get_conf_dir_hierarchy(monkeypatch: pytest.MonkeyPatch):
    """Tests hierarchy of versioning for config"""
    config_paths = ['config_path/one', 'config_path/two']
    expected = [
        ('config_path/one/jupyter_config.py'),
        ('config_path/one/0/jupyter_config.py'),
        ('config_path/one/0.6/jupyter_config.py'),
        ('config_path/one/0.6.0/jupyter_config.py'),
        ('config_path/two/jupyter_config.py'),
        ('config_path/two/0/jupyter_config.py'),
        ('config_path/two/0.6/jupyter_config.py'),
        ('config_path/two/0.6.0/jupyter_config.py')
    ]
    monkeypatch.setattr(config_util, '__version__', '0.6.0')
    actual = get_conf_dir_hierarchy(config_paths)
    assert actual == expected
