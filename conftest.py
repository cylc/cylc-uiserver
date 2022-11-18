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

pytest_plugins = [
    'jupyter_server.pytest_plugin'
]


ignore_collect = [
    # jupyterhub stuff messes with the environment
    'cylc/uiserver/hubapp.py',
    'cylc/uiserver/scripts/hubapp.py',
    'cylc/uiserver/scripts/hub.py',
    # the jupyter config cannot be imported
    'cylc/uiserver/jupyter_config.py',
]


def pytest_ignore_collect(path):
    # --doctest-modules seems to ignore the value if configured in pyproject
    return any(
        ignore_path in str(path)
        for ignore_path in ignore_collect
    )
