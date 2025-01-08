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

__version__ = "1.6.0"

import os
from typing import Dict
from cylc.uiserver.app import CylcUIServer

from cylc.uiserver.logging_util import RotatingUISFileHandler


def init_log():
    LOG = RotatingUISFileHandler()
    # set up uiserver log
    LOG.on_start()


def _jupyter_server_extension_points():
    """
    Returns a list of dictionaries with metadata describing
    where to find the `_load_jupyter_server_extension` function.
    """
    return [
        {
            "module": "cylc.uiserver.app",
            'app': CylcUIServer
        }
    ]


def getenv(*env_vars: str) -> Dict[str, str]:
    """Extract env vars if set.

    Returns a dict containing key:value pairs of environment variables
    defined in env_vars providing they are present in the environment.

    Examples:
        >>> getenv('HOME', 'NOT_AN_ENVIRONMENT_VARIABLE')
        {'HOME': ...}

    """
    env: Dict[str, str] = {}
    for env_var in env_vars:
        if env_var in os.environ:
            env[env_var] = os.environ[env_var]
    return env
