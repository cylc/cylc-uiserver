# Copyright (C) Earth Sciences New Zealand & British Crown (Met Office)
# & Contributors.
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

from contextlib import suppress
from logging.handlers import RotatingFileHandler
from pathlib import Path


# Global var to track whether logging has been started before.
# This is needed as Traitlets may reconfigure logging several times
# within the lifetime of the application, which creates new instances
# of the handler.
log_started = False


class RotatingUISFileHandler(RotatingFileHandler):
    """Rotate logs on ui-server restart or when reaching maxBytes."""

    def __init__(self, filename: str, *args, **kwargs):
        global log_started
        if log_started:
            do_initial_rollover = False
        else:
            log_started = True
            do_initial_rollover = Path(filename).is_file()

        # Ensure the log directory exists:
        Path(filename).parent.mkdir(parents=True, exist_ok=True)

        super().__init__(filename, *args, **kwargs)
        if do_initial_rollover:
            self.doRollover()

        # BACK COMPAT: Remove any log files under old naming schemes
        # to: 1.10.x
        # remove at: 1.12
        log_dir = Path(filename).parent
        for old_log in log_dir.glob('[0-9][0-9]-uiserver.log'):
            # old-style log files
            with suppress(OSError):
                old_log.unlink()
        for old_log in (log_dir / 'log', *log_dir.glob('log.[0-9]')):
            # old-style rotated filenames
            with suppress(OSError):
                old_log.unlink()

    def rotation_filename(self, default_name: str) -> str:
        """Override the default naming scheme.

        Args:
            default_name: By default, RotatingFileHandler passes this in
                as <base-file-path>.<num>
        """
        _path, _num = default_name.rsplit(".", 1)
        path = Path(_path)
        # The rotation num should be 1 higher to account for the fact that
        # we include `-01` in the initial log file name
        num = int(_num) + 1
        return str(
            path.parent
            / f"{path.stem.removesuffix('-01')}-{num:02d}{path.suffix}"
        )
