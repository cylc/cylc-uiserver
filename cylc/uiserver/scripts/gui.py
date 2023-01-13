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

from ansimarkup import parse as cparse
import argparse
import asyncio
from contextlib import suppress
from glob import glob
import os
from pathlib import Path
import random
import re
import sys
import webbrowser


from cylc.flow.id_cli import parse_id_async
from cylc.flow.exceptions import (
    InputError,
    WorkflowFilesError
)

from cylc.uiserver import init_log
from cylc.uiserver.app import (
    CylcUIServer,
    INFO_FILES_DIR
)

CLI_OPT_NEW = "--new"


def main(*argv):
    init_log()
    jp_server_opts, new_gui, workflow_id = parse_args_opts()
    if '--help' not in sys.argv:
        # get existing jpserver-<pid>-open.html files
        # assume if this exists then the server is still running
        # these files are cleaned by jpserver on shutdown
        existing_guis = glob(os.path.join(INFO_FILES_DIR, "*open.html"))
        if existing_guis and not new_gui:
            gui_file = random.choice(existing_guis)
            print(
                "Opening with existing gui." +
                f" Use {CLI_OPT_NEW} option for a new gui.",
                file=sys.stderr
            )
            update_html_file(gui_file, workflow_id)
            if '--no-browser' not in sys.argv:
                webbrowser.open(gui_file, autoraise=True)
            return
    return CylcUIServer.launch_instance(
        jp_server_opts or None, workflow_id=workflow_id
    )


def print_error(error: str, msg: str):
    """Print formatted error with message"""
    print(cparse(
        f'<red><bold>{error}: </bold>{msg}</red>'
    ), file=sys.stderr
    )


def parse_args_opts():
    """Parse cli args

    Separate JPserver args from Cylc specific ones.
    Parse workflow id.
    Raise error if invalid workflow provided
    """
    cylc_opts, jp_server_opts = get_arg_parser().parse_known_args()
    # gui arg is stripped cylc end but need to re-strip after arg parsing here
    with suppress(ValueError):
        jp_server_opts.remove('gui')
    new_gui = cylc_opts.new
    if new_gui:
        sys.argv.remove(CLI_OPT_NEW)
    workflow_id = None
    workflow_arg = [
        arg for arg in jp_server_opts
        if not arg.startswith('-')
    ]
    if len(workflow_arg) > 1:
        msg = "Wrong number of arguments (too many)"
        print_error("CylcError", msg)
        sys.exit(1)
    if len(workflow_arg) == 1:
        try:
            loop = asyncio.new_event_loop()
            task = loop.create_task(parse_id_async(
                workflow_arg[0], constraint='workflows'))
            loop.run_until_complete(task)
            loop.close()
            workflow_id, _, _ = task.result()
        except (InputError, WorkflowFilesError) as exc:
            # workflow not found
            print_error(exc.__class__.__name__, exc)
            sys.exit(1)

    # Remove args which are workflow ids from jp_server_opts.
    jp_server_opts = tuple(
        arg for arg in jp_server_opts if arg not in workflow_arg)
    [sys.argv.remove(arg) for arg in workflow_arg]
    return jp_server_opts, new_gui, workflow_id


def get_arg_parser():
    """Cylc specific options"""
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument(
        CLI_OPT_NEW,
        action='store_true',
        default=False,
        dest='new'
    )
    return parser


def update_html_file(gui_file, workflow_id):
    """ Update the html file to open at the correct workflow in the gui.
    """
    with open(gui_file, "r") as f:
        file_content = f.read()
    url_extract_regex = re.compile('url=(.*?)\"')
    url_string = url_extract_regex.search(file_content)
    if not url_string:
        return
    url = url_string.group(1)
    split_url = url.split('/workflows/')
    if not workflow_id:
        # new url should point to dashboard
        if len(split_url) == 1:
            # no update required
            return
        else:
            # previous url points to workflow page and needs updating
            # replace with base url (including token)
            replacement_url_string = split_url[0]
    else:
        if len(split_url) > 1:
            old_workflow = split_url[1]
            if workflow_id == old_workflow:
                # same workflow page requested, no update needed
                return
            else:
                replacement_url_string = url.replace(old_workflow, workflow_id)
        else:
            # current url points to dashboard, update to point to workflow
            replacement_url_string = f"{url}/workflows/{workflow_id}"
    update_url_string(gui_file, url, replacement_url_string)


def update_url_string(gui_file: str, url: str, replacement_url_string: str):
    """Updates the url string in the given gui file."""
    file = Path(gui_file)
    current_text = file.read_text()
    updated_text = current_text.replace(url, replacement_url_string)
    file.write_text(updated_text)
