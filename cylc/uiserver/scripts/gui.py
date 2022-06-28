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

import asyncio
import os
import sys

from pathlib import Path
from psutil import pid_exists

from cylc.flow.id_cli import parse_id_async
from cylc.flow.exceptions import InputError

from cylc.uiserver import init_log
from cylc.uiserver.app import CylcUIServer


def main(*argv):
    init_log()
    pid_file = Path("~/.cylc/uiserver/pid").expanduser()
    check_pid(pid_file)
    create_pid_file(pid_file)

    workflow_id = None
    for arg in argv:
        if arg.startswith('-'):
            continue
        try:
            loop = asyncio.new_event_loop()
            task = loop.create_task(
                parse_id_async(
                    arg, constraint='workflows'))
            loop.run_until_complete(task)
            loop.close()
            workflow_id, _, _ = task.result()
            argv = tuple(x for x in argv if x != arg)
            sys.argv.remove(arg)
        except InputError:
            print(f"Workflow '{arg}' does not exist.")
            break
    return CylcUIServer.launch_instance(argv or None, workflow_id=workflow_id)


def check_pid(pid_file: Path):
    """Check for process_id file.

    Raises exception if gui is currently running with active process id.
    """
    if not pid_file.is_file():
        return
    else:
        pid = pid_file.read_text()
        try:
            if pid_exists(int(pid)):
                raise Exception(f"cylc gui is running at process id: {pid}")
        except (TypeError, ValueError):
            try:
                pid_file.unlink()
                print(f"Deleting corrupt process id file. {pid_file.parent}")
            except FileNotFoundError:
                pass


def create_pid_file(pid_file: Path):
    """Write current process to process id file."""
    pid = os.getpid()
    with open(pid_file, "w") as f:
        f.write(str(pid))
