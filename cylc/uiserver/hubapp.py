# Copyright (c) 2015 Project Jupyter Contributors
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice,
#    this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its
#    contributors may be used to endorse or promote products derived from
#    this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
#
# Semver File License
# ===================
#
# The semver.py file is from https://github.com/podhmo/python-semver
# which is licensed under the "MIT" license.  See the semver.py file for
# details.
"""Launch the Cylc GUI.

Acknowledgment derived from the Jupyter Lab source code:
https://github.com/jupyterlab/jupyterlab/blob/v3.0.16/jupyterlab/labhubapp.py
"""

import os
import sys

from jupyter_server.serverapp import ServerApp
from traitlets import default

from cylc.uiserver.app import CylcUIServer


if not os.environ.get("JUPYTERHUB_SINGLEUSER_APP"):
    # setting this env prior to import of jupyterhub.singleuser
    # avoids unnecessary import of notebook
    os.environ["JUPYTERHUB_SINGLEUSER_APP"] = (
        "jupyter_server.serverapp.ServerApp"
    )

try:
    from jupyterhub.singleuser.mixins import make_singleuser_app
except ImportError:
    # backward-compat with jupyterhub < 1.3
    from jupyterhub.singleuser import (
        SingleUserNotebookApp as SingleUserServerApp
    )
else:
    SingleUserServerApp = make_singleuser_app(ServerApp)


class CylcHubApp(SingleUserServerApp):
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
