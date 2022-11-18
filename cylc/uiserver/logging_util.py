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

from contextlib import suppress
from glob import glob
import logging
import os
from pathlib import Path

from typing import List

from cylc.uiserver.app import USER_CONF_ROOT


class RotatingUISFileHandler(logging.handlers.RotatingFileHandler):
    """Rotate logs on ui-server restart"""

    LOG_NAME_EXTENSION = "-uiserver.log"

    def __init__(self):
        self.file_path = Path(USER_CONF_ROOT / "log").expanduser()

    def on_start(self):
        """Set up logging"""
        self.file_path.mkdir(parents=True, exist_ok=True)
        self.delete_symlink()
        self.update_log_archive()
        self.setup_new_log()

    def update_log_archive(self):
        """Ensure log archive retains only 5 logs"""
        log_files = sorted(glob(os.path.join(
            self.file_path, f"[0-9]*{self.LOG_NAME_EXTENSION}")), reverse=True)
        while len(log_files) > 4:
            os.unlink(log_files.pop(0))
        # rename logs, logs sent in descending order to prevent conflicts
        self.rename_logs(log_files)

    def rename_logs(self, log_files: List[str]):
        """Increment the log number by one for each log"""
        for file in log_files:
            log_num = int(Path(file).name.partition('-')[0]) + 1
            new_file_name = Path(
                f"{self.file_path}/{log_num:02d}{self.LOG_NAME_EXTENSION}"
            )
            Path(file).rename(new_file_name)

    def delete_symlink(self):
        """Deletes an existing log symlink."""
        symlink_path = Path(self.file_path / 'log')
        if symlink_path.exists() and symlink_path.is_symlink():
            symlink_path.unlink()

    def setup_new_log(self):
        """Create log"""
        log = Path(self.file_path / f'01{self.LOG_NAME_EXTENSION}')
        log.touch()
        symlink_path = Path(self.file_path / 'log')
        with suppress(OSError):
            symlink_path.symlink_to(log)
