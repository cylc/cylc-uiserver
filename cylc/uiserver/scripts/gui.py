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

import sys

# from cylc.flow.id_cli import parse_id, parse_id_async
from cylc.flow.exceptions import InputError

from cylc.uiserver import init_log
from cylc.uiserver.app import CylcUIServer


def main(*argv):
    init_log()
    workflow_id = None
    for arg in argv:
        if arg.startswith('-'):
            continue
        try:
            # workflow_id, _, _ = parse_id(
            # arg, constraint='workflows', infer_latest_runs=True)

            # The following line needs to be replaced with the line above in
            # order to interpret the workflow_id. This, causes problems with
            # the ServerApp Event loop.

            workflow_id = arg
            argv = tuple(x for x in argv if x != arg)
            sys.argv.remove(arg)
        except InputError:
            print(f"Workflow '{arg}' does not exist.")
            break
    return CylcUIServer.launch_instance(argv or None, workflow_id=workflow_id)
