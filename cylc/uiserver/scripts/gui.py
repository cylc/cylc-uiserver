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
import re
from requests.exceptions import RequestException
import requests
import sys
from textwrap import dedent
from typing import Optional
import webbrowser
from getpass import getuser


from cylc.flow.id_cli import parse_id_async
from cylc.flow.exceptions import (
    InputError,
    WorkflowFilesError
)

from cylc.flow.cfgspec.glbl_cfg import glbl_cfg

from cylc.uiserver import init_log
from cylc.uiserver.app import (
    CylcUIServer,
    INFO_FILES_DIR
)

CLI_OPT_NEW = "--new"


def main(*argv):
    init_log()
    hub_url = glbl_cfg().get(['hub', 'url'])
    jp_server_opts, new_gui, workflow_id = parse_args_opts()
    if '--help' in sys.argv and hub_url:
        print(
            dedent('''
                cylc gui [WORKFLOW]

                Open the Cylc GUI in a new web browser tab.

                If WORKFLOW is specified, the GUI will open on this workflow.

                This command has been configured to use a centrally configured
                Jupyter Hub instance rather than start a standalone server.
                To see the configuration options for the server run
                "cylc gui --help-all", these options can be configured in the
                Jupyter configuration files using "c.Spawner.cmd", see the Cylc
                and Jupyter Hub documentation for more details.
            '''))
        return
    if not {'--help', '--help-all'} & set(sys.argv):
        if hub_url:
            print(f"Running on {hub_url } as specified in global config.")
            webbrowser.open(
                update_url(hub_url, workflow_id), autoraise=True
            )
            return
        # get existing jpserver-<pid>-open.html files
        # check if the server is available for use
        # prompt for user whether to clean files for un-usable uiservers
        # these files are usually cleaned by jpserver on shutdown, although
        # can be left behind on crash or a `kill -9` of the process
        existing_guis = glob(os.path.join(INFO_FILES_DIR, "*open.html"))
        if existing_guis and not new_gui:
            url = select_info_file(existing_guis)
            if url:
                print(
                    "Opening with existing gui." +
                    f" Use {CLI_OPT_NEW} option to start a new gui server.",
                    file=sys.stderr
                )
                url = update_url(url, workflow_id)
                if '--no-browser' not in sys.argv:
                    webbrowser.open(url, autoraise=True)
                return
    return CylcUIServer.launch_instance(
        jp_server_opts or None, workflow_id=workflow_id
    )


def select_info_file(existing_guis: list) -> Optional[str]:
    """This will select an active ui-server info file"""
    existing_guis.sort(key=os.path.getmtime, reverse=True)
    for gui_file in existing_guis:
        url = get_url_from_file(gui_file)
        if url and is_active_gui(url):
            return url
        check_remove_file(gui_file)
    return None


def get_url_from_file(gui_file):
    with open(gui_file, "r") as f:
        file_content = f.read()
    url_extract_regex = re.compile('url=(.*?)\"')
    match = url_extract_regex.search(file_content)
    return match.group(1) if match else None


def is_active_gui(url: str) -> bool:
    """Returns true if return code is 200 from server"""
    try:
        return requests.get(url).status_code == 200
    except RequestException:
        return False


def clean_info_files(gui_file):
    pid = re.compile(r'-(\d*)-open\.html').search(gui_file).group(1)
    json_file = os.path.join(INFO_FILES_DIR, f"jpserver-{pid}.json")
    with suppress(OSError):
        os.unlink(gui_file)
    with suppress(OSError):
        os.unlink(json_file)


def check_remove_file(gui_file) -> None:
    """Ask user if they want to remove the file."""
    print("The following file cannot be used to open the Cylc GUI:"
          f" {gui_file}.\nThe ui-server may be running on another host,"
          " or it may be down.")
    ret = input(
        cparse('<yellow>Do you want to remove this file? (y/n):</yellow>'))
    if ret.lower() == 'y':
        clean_info_files(gui_file)
    return


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


def update_url(url, workflow_id):
    """ Update the url to open at the correct workflow in the gui.
    """
    hub_url = glbl_cfg().get(['hub', 'url'])
    if not url:
        return
    split_url = url.split('/workspace/')
    if not workflow_id:
        # new url should point to dashboard
        if len(split_url) == 1:
            # no update required
            return url
        else:
            # previous url points to workflow page and needs updating
            # replace with base url (including token)
            return split_url[0]
    else:
        if len(split_url) > 1:
            old_workflow = split_url[1]
            if workflow_id == old_workflow:
                # same workflow page requested, no update needed
                return url
            else:
                return url.replace(old_workflow, workflow_id)
        else:
            # current url points to dashboard, update to point to workflow
            if hub_url:
                return (f"{url}/user/{getuser()}/{CylcUIServer.name}"
                        f"/#/workspace/{workflow_id}")
            else:
                return f"{url}/workspace/{workflow_id}"
