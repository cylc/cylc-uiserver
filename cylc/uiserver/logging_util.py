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

from logging.handlers import RotatingFileHandler
from pathlib import Path


class RotatingUISFileHandler(RotatingFileHandler):
    """Rotate logs on ui-server restart or when reaching maxBytes."""

    # Class attribute to track whether logging has been started before.
    # This is needed as Traitlets may reconfigure logging several times
    # within the lifetime of the application, which creates new instances
    # of the handler.
    started = False

    def __init__(self, filename, *args, **kwargs):
        if RotatingUISFileHandler.started:
            do_initial_rollover = False
        else:
            RotatingUISFileHandler.started = True
            do_initial_rollover = Path(filename).is_file()
        super().__init__(filename, *args, **kwargs)
        if do_initial_rollover:
            self.doRollover()
