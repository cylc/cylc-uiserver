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
"""cylc hub

Launch the Cylc hub for running the Cylc Web GUI.
"""

import os
import sys
from unittest.mock import patch
from pathlib import Path

from jupyterhub.app import JupyterHub

from cylc.uiserver import (
    __version__,
    __file__ as uis_pkg
)


def main(*args):
    for arg in args:
        if arg.startswith('-f') or arg.startswith('--config'):
            break
    else:
        config_file = Path(uis_pkg).parent / 'jupyterhub_config.py'
        args = (f'--config={config_file}',) + args
    # set an env var flag to help load the config
    os.environ['CYLC_HUB_VERSION'] = __version__
    try:
        # JupyterHub 3.0.0 incorrectly passes our config file path as second
        # arg of Tornado run_sync, which is supposed to be a timeout value.
        #   https://github.com/jupyterhub/jupyterhub/pull/4039
        # Reviewer: "Will do a 3.0.1 pretty soon after some more 3.0 feedback."
        # TODO: once we depend on jupyter >= 3.0.1 can revert to this:
        #   JupyterHub.launch_instance(args)
        with patch.object(sys, "argv", [sys.argv[0]] + list(args)):
            # Patch works via traitlets.config.Application.parse_command_line
            JupyterHub.launch_instance()
    finally:
        del os.environ['CYLC_HUB_VERSION']
