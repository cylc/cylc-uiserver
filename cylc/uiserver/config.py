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
"""Provides a loader function for fetching the Jupyterhub config.

This provides the logic for loading user configurations from the .cylc dir.

Note: Jupyterhub configs cannot be imported directly due to the way Jupyterhub
provides the configuration object to the file when it is loaded.

"""
import logging
import os
from pathlib import Path

from cylc.uiserver import __file__ as uis_pkg

LOG = logging.getLogger(__name__)

# base configuration - always used
DEFAULT_CONF_PATH: Path = Path(uis_pkg).parent / 'config_defaults.py'
# site configuration
SITE_CONF_PATH: Path = Path('/etc/cylc/hub/config.py')
# user configuration
USER_CONF_PATH: Path = Path('~/.cylc/hub/config.py').expanduser()


def _load(path):
    """Load a configuration file."""
    if path.exists():
        LOG.info(f'Loading config file: {path}')
        exec(path.read_text())


def load():
    """Load the relevant UIS/Hub configuration files."""
    if os.getenv('CYLC_SITE_CONF_PATH'):
        site_conf_path: Path = Path(
            os.environ['CYLC_SITE_CONF_PATH'],
            'hub/config.py'
        )
    else:
        site_conf_path: Path = SITE_CONF_PATH
    config_paths = [DEFAULT_CONF_PATH, site_conf_path, USER_CONF_PATH]
    for path in config_paths:
        _load(path)


if 'CYLC_HUB_VERSION' in os.environ:
    # auto-load the config (jupyterhub requirement)
    # the env var prevents the config from being loaded on import
    load()
