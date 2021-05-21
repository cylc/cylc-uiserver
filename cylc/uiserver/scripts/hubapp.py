"""Command for launching the Cylc GUI in its JupyterHub configuration.

This should be the command JupyterHub is configured to spawn e.g:
  c.Spawner.cmd = ['cylc', 'hubapp']
"""

from cylc.uiserver.hubapp import CylcHubApp

INTERNAL = True


def main(*argv):
    return CylcHubApp.launch_instance(argv or None)
