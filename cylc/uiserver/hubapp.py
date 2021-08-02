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
"""Launch the Cylc GUI.

This code packages the CylcUIServer to hook it into JupyterHub:

Acknowledgment:
    Code derived from the Jupyter Lab source (BSD).

    Copyright (c) 2015 Project Jupyter Contributors
    All rights reserved.

    https://github.com/jupyterlab/jupyterlab/blob/v3.0.16/jupyterlab/
        labhubapp.py
"""

import os
import sys


if not os.environ.get("JUPYTERHUB_SINGLEUSER_APP"):
    # setting this env prior to import of jupyterhub.singleuser
    # avoids unnecessary import of notebook
    os.environ["JUPYTERHUB_SINGLEUSER_APP"] = (
        "jupyter_server.serverapp.ServerApp"
    )


# NOTE: import after setting JUPYTERHUB_SINGLEUSER_APP
from jupyter_server.serverapp import ServerApp
from jupyterhub.singleuser.mixins import make_singleuser_app
from traitlets import default

from cylc.uiserver.app import CylcUIServer


SingleUserServerApp = make_singleuser_app(ServerApp)  # type: ignore


class CylcHubApp(SingleUserServerApp):  # type: ignore
    """The CylcUIServer app configured for use with JupyterHub."""

    @default("default_url")
    def _default_url(self):
        # redirect users to the cylc endpoint on launch
        return "/cylc"

    def find_server_extensions(self):
        """Unconditionally enable Cylc server extension.

        Never called if using legacy SingleUserNotebookApp.
        """
        super().find_server_extensions()
        self.jpserver_extensions[CylcUIServer.get_extension_package()] = True

    @classmethod
    def launch_instance(cls, argv=None, **kwargs):
        if argv is None and sys.argv[0].endswith('cylc'):
            # jupyter server isn't expecting to be launched by a Cylc command
            # this patches some internal logic to leave just the args for
            # the server
            argv = sys.argv[2:]
        super().launch_instance(argv=argv, **kwargs)
