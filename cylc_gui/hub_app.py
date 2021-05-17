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
"""Launch the Cylc GUI."""

import os
import sys

from jupyter_server.serverapp import ServerApp
from traitlets import default

from cylc_gui import CylcGUI


if not os.environ.get("JUPYTERHUB_SINGLEUSER_APP"):
    # setting this env prior to import of jupyterhub.singleuser avoids unnecessary import of notebook
    os.environ["JUPYTERHUB_SINGLEUSER_APP"] = "jupyter_server.serverapp.ServerApp"

try:
    from jupyterhub.singleuser.mixins import make_singleuser_app
except ImportError:
    # backward-compat with jupyterhub < 1.3
    from jupyterhub.singleuser import SingleUserNotebookApp as SingleUserServerApp
else:
    SingleUserServerApp = make_singleuser_app(ServerApp)


class SingleUserCylcGUI(SingleUserServerApp):
    @default("default_url")
    def _default_url(self):
        return "/cylc"

    def find_server_extensions(self):
        """unconditionally enable jupyterlab server extension
        never called if using legacy SingleUserNotebookApp
        """
        super().find_server_extensions()
        self.jpserver_extensions[CylcGUI.get_extension_package()] = True

    @classmethod
    def launch_instance(cls, argv=None, **kwargs):
        if argv is None:
            # jupyter server isn't expecting to be launched by a Cylc command
            # this patches some internal logic
            argv = sys.argv[2:]
        super().launch_instance(argv=argv, **kwargs)


def main(argv=None):
    argv = None
    return SingleUserCylcGUI.launch_instance(argv)
