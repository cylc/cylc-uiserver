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
from pathlib import Path
from functools import partial

from jupyterhub.app import JupyterHub
from tornado.ioloop import IOLoop

from cylc.uiserver import (
    __version__,
    __file__ as uis_pkg
)


def launch_instance(cls, argv=None):
    """JupyterHub class method to correctly pass argv to launch_instance_async.

    At JupyterHub 3.0.0 this incorrectly passes our config file path as second
    arg of Tornado run_sync, which is supposed to be a timeout value.
    """
    self = cls.instance()
    self._init_asyncio_patch()
    loop = IOLoop(make_current=False)
    try:
        # bug: loop.run_sync(self.launch_instance_async, argv)
        loop.run_sync(partial(self.launch_instance_async, argv))
    except Exception:
        loop.close()
        raise
    try:
        loop.start()
    except KeyboardInterrupt:
        print("\nInterrupted")
    finally:
        loop.stop()
        loop.close()


# Patch JupyterHub to use our bug-fix version of launch_instance.
JupyterHub.launch_instance = classmethod(launch_instance)


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
        JupyterHub.launch_instance(args)
    finally:
        del os.environ['CYLC_HUB_VERSION']
