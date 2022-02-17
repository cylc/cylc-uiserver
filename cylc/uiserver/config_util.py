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
"""Utility functions for config loading.
"""

from itertools import product
import os
from pathlib import Path
from typing import Iterable, List, Union

from cylc.flow.cfgspec.globalcfg import (
    GlobalConfig,
    get_version_hierarchy
)
from cylc.uiserver import (
    __file__ as uis_pkg,
    __version__
)

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


def get_conf_dir_hierarchy(
    config_paths: Iterable[Union[Path, str]], filename: bool = True
) -> List[str]:
    """Takes list of config paths, adds version and filename to the path"""
    conf_hierarchy = []
    version_hierarchy = get_version_hierarchy(__version__)
    for x in product(config_paths, version_hierarchy):
        if filename:
            conf_hierarchy.append(
                str(Path(x[0], x[1], 'jupyter_config.py').expanduser()))
        else:
            conf_hierarchy.append(str(Path(x[0], x[1])))
    return conf_hierarchy
