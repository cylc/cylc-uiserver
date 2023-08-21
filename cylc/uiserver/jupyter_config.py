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

# Configuration file for jupyterhub.

from pathlib import Path
import pkg_resources

from cylc.uiserver import (
    __file__ as uis_pkg,
    getenv)
from cylc.uiserver.app import USER_CONF_ROOT
from cylc.uiserver.authorise import CylcAuthorizer


# the command the hub should spawn (i.e. the cylc uiserver itself)
c.Spawner.cmd = ['cylc', 'hubapp']

# the spawner to invoke this command
c.JupyterHub.spawner_class = 'jupyterhub.spawner.LocalProcessSpawner'

# environment variables to pass to the spawner (if defined)
c.Spawner.environment = getenv(
    # site config path override
    'CYLC_SITE_CONF_PATH',
    # used to specify the Cylc version if using a wrapper script
    'CYLC_VERSION',
    'CYLC_ENV_NAME',
    # may be used by Cylc UI developers to use a development UI build
    'CYLC_DEV',
)
# this auto-spawns uiservers without user interaction
c.JupyterHub.implicit_spawn_seconds = 0.01

# apply cylc styling to jupyterhub
c.JupyterHub.logo_file = str(Path(uis_pkg).parent / 'logo.svg')
c.JupyterHub.log_datefmt = '%Y-%m-%dT%H:%M:%S'  # ISO8601 (expanded)
c.JupyterHub.template_paths = [
    # custom HTML templates
    pkg_resources.resource_filename(
        'cylc.uiserver',
        'templates'
    )
]

# store JupyterHub runtime files in the user config directory
USER_CONF_ROOT.mkdir(parents=True, exist_ok=True)
c.JupyterHub.cookie_secret_file = f'{USER_CONF_ROOT / "cookie_secret"}'
c.JupyterHub.db_url = f'{USER_CONF_ROOT / "jupyterhub.sqlite"}'
c.ConfigurableHTTPProxy.pid_file = f'{USER_CONF_ROOT / "jupyterhub-proxy.pid"}'

# write Cylc logging to the user config directory
# NOTE: Parallel UIS instances will conflict over this file.
#       See https://github.com/cylc/cylc-uiserver/issues/240
c.CylcUIServer.logging_config = {
    'version': 1,
    'handlers': {
        'file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'level': 'INFO',
            'filename': str(USER_CONF_ROOT / 'log' / 'log'),
            'mode': 'a',
            'backupCount': 5,
            'maxBytes': 10485760,
            'formatter': 'file_fmt',
        },
    },
    'loggers': {
        'CylcUIServer': {
            'level': 'INFO',
            'handlers': ['console', 'file'],
        },
        'cylc': {
            'level': 'INFO',
            'handlers': ['console', 'file'],
        },
    },
    'formatters': {
        'file_fmt': {
            'format': '%(asctime)s %(levelname)-8s %(message)s',
            'datefmt': '%Y-%m-%dT%H:%M:%S',
        }
    },
}


# Define the authorization-policy for Jupyter Server.
# This prevents users being granted full access to extensions such as Jupyter
# Lab as a result of being granted the ``access:servers`` permission in Jupyter
# Hub.
c.ServerApp.authorizer_class = CylcAuthorizer
