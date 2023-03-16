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
"""Command for launching the Cylc GUI in its JupyterHub configuration.

This should be the command JupyterHub is configured to spawn e.g:
  c.Spawner.cmd = ['cylc', 'hubapp']
"""

from cylc.uiserver import init_log
from cylc.uiserver.hubapp import CylcHubApp

INTERNAL = True


def main(*argv):
    init_log()
    return CylcHubApp.launch_instance(argv or None)
