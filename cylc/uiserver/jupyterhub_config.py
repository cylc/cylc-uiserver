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
from itertools import product
import logging
import os
from pathlib import Path
from typing import List, Optional

from cylc.flow.cfgspec.globalcfg import (
    GlobalConfig,
    get_version_hierarchy
)

from cylc.uiserver import (
    __file__ as uis_pkg,
    __version__
)


LOG = logging.getLogger(__name__)

# base configuration - always used
DEFAULT_CONF_PATH: Path = Path(uis_pkg).parent / 'jupyter_config.py'
UISERVER_DIR = 'uiserver'
# UIS configuration dirs
SITE_CONF_ROOT: Path = Path(
    os.getenv('CYLC_SITE_CONF_PATH')
    or GlobalConfig.DEFAULT_SITE_CONF_PATH,
    UISERVER_DIR
)
USER_CONF_ROOT = Path.home() / '.cylc' / UISERVER_DIR


def _load(path):
    """Load a configuration file."""
    if path.exists():
        LOG.info(f'Loading config file: {path}')
        exec(path.read_text())


def get_conf_dir_hierarchy(
        config_paths: List[Path], filename: bool = True
) -> List[Path]:
    """Takes list of config paths, adds version and filename to the path"""
    conf_hierarchy = []
    version_hierarchy = get_version_hierarchy(hub_version or __version__)
    for x in product(config_paths, version_hierarchy):
        if filename:
            conf_hierarchy.append(Path(x[0], x[1], 'jupyter_config.py'))
        else:
            conf_hierarchy.append(Path(x[0], x[1]))
    return conf_hierarchy


def load() -> None:
    """Load the relevant UIS/Hub configuration files."""
    if os.getenv('CYLC_SITE_CONF_PATH'):
        site_conf_path: Path = Path(
            os.environ['CYLC_SITE_CONF_PATH'],
            UISERVER_DIR
        )
    else:
        site_conf_path = SITE_CONF_ROOT
    base_config_paths = [site_conf_path, USER_CONF_ROOT]
    # add versioning to paths
    config_paths = get_conf_dir_hierarchy(base_config_paths)
    # Default conf path not currently versioned:
    config_paths.insert(0, DEFAULT_CONF_PATH)
    for path in config_paths:
        _load(path)


hub_version = os.environ.get('CYLC_HUB_VERSION')
if hub_version:
    # auto-load the config (jupyterhub requirement)
    # the env var prevents the config from being loaded on import
    load()
