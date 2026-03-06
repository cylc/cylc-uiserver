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
from typing import Iterable, List, Literal, Union

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
    config_paths: Iterable[Union[Path, str]],
    component_name: Literal['hub', 'cylc'],
    directory_only: bool = False,
) -> List[str]:
    """Returns a list of Jupyter configuration files to load.

    * Cylc configuration files may be located in a hierarchy determined by the
      version number.
    * Jupyter configuration files differ depending on the component they are
      loaded by.

    This function expands the hierarchy to return the full list of filesystem
    locations where configuration files may reside.

    Args:
        config_paths:
            The root configuration directories to search for configuration
            files in.
        component_name:
            The name of Jupyter component which is loading these configuration
            files, e.g, "hub" (JupyterHub) or "cylc" (CylcUIServer).
        directory_only:
            If True, only the directories (to search for files in) will be
            output, otherwise, the full filepath of each file will be listed.

    """
    conf_hierarchy = []
    version_hierarchy = get_version_hierarchy(__version__)
    for x in product(config_paths, version_hierarchy):
        directory = Path(x[0], x[1]).expanduser()
        if directory_only:
            conf_hierarchy.append(str(directory))
        else:
            conf_hierarchy.extend([
                str(directory / 'jupyter_config.py'),
                str(directory / f'jupyter{component_name}_config.py'),
            ])

    return conf_hierarchy
