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
import os
from pathlib import Path

from cylc.uiserver import __file__ as uis_pkg


DEFAULT_CONF_PATH = Path(uis_pkg).parent / 'config_defaults.py'
USER_CONF_PATH = Path('~/.cylc/hub/config.py').expanduser()


def load():
    config_paths = [DEFAULT_CONF_PATH, USER_CONF_PATH]
    for path in config_paths:
        if path.exists():
            exec(path.read_text())


if 'CYLC_HUB_VERSION' in os.environ:
    # prevent the config from being loaded on import
    load()
