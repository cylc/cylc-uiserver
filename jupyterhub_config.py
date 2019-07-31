# -*- coding: utf-8 -*-
# Copyright (C) 2019 NIWA & British Crown (Met Office) & Contributors.
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


HERE = Path(__file__).resolve().parent
DIST = HERE.joinpath(Path('../cylc-ui/dist'))


# --- Extra arguments to be passed to the single-user server.

#  Some spawners allow shell-style expansion here, allowing you to use
#  environment variables here. Most, including the default, do not. Consult the
#  documentation for your spawner to verify!
c.Spawner.args = ['-s', str(DIST)]

#  Some spawners allow shell-style expansion here, allowing you to use
#  environment variables. Most, including the default, do not. Consult the
#  documentation for your spawner to verify!
c.Spawner.cmd = ['cylc-uiserver']

# --- Specify path to a logo image to override the Jupyter logo in the banner.

c.JupyterHub.logo_file = str(DIST.joinpath(Path('img/logo.png')))

# --- The class to use for spawning single-user servers.

#  Should be a subclass of Spawner.
c.JupyterHub.spawner_class = 'jupyterhub.spawner.LocalProcessSpawner'
