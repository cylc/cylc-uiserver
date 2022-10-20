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

"""cylc gui [OPTIONS]

Launch the Cylc GUI as a standalone web app for local use.

For a multi-user system see `cylc hub`.
"""

from cylc.uiserver import init_log
from cylc.uiserver.app import CylcUIServer


def main(*argv):
    init_log()
    return CylcUIServer.launch_instance(argv or None)
