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

from glob import glob
import os
import pytest

from pathlib import Path

from cylc.uiserver.logging_util import RotatingUISFileHandler


def test_update_log_archive(tmp_path):
    """Test update log archive retains log count at 5"""
    LOG = RotatingUISFileHandler()
    LOG.file_path = Path(tmp_path/'.cylc'/'uiserver'/'log')
    LOG.file_path.mkdir(parents=True, exist_ok=True)
    for file in [
        '03-uiserver.log',
        '01-uiserver.log',
        '04-uiserver.log',
        '02-uiserver.log',
        '05-uiserver.log',
        '07-uiserver.log',
        '06-uiserver.log'
    ]:
        log_file = LOG.file_path.joinpath(file)
        log_file.touch()

    LOG.update_log_archive()
    log_files = glob(os.path.join(LOG.file_path, f"[0-9]*.log"))
    expected_files = [
        f'{LOG.file_path}/05-uiserver.log',
        f'{LOG.file_path}/04-uiserver.log',
        f'{LOG.file_path}/03-uiserver.log',
        f'{LOG.file_path}/02-uiserver.log',
    ]
    assert len(log_files) == 4
    assert sorted(log_files) == sorted(expected_files)


def test_setup_new_log(tmp_path):
    """Checks new log is set up correctly."""
    LOG = RotatingUISFileHandler()
    LOG.file_path = Path(tmp_path/'.cylc'/'uiserver'/'log')
    LOG.file_path.mkdir(parents=True, exist_ok=True)
    LOG.setup_new_log()
    new_log = Path(LOG.file_path / '01-uiserver.log')
    symlink_log = Path(LOG.file_path / 'log')
    assert new_log.exists()
    assert symlink_log.is_symlink()
    assert symlink_log.resolve() == new_log


def test_first_init_log(tmp_path):
    """Check initial setup, no previous logs present"""
    LOG = RotatingUISFileHandler()
    LOG.file_path = Path(tmp_path/'.cylc'/'uiserver'/'log')
    LOG.on_start()
    assert LOG.file_path.exists()
    assert Path(LOG.file_path / 'log').is_symlink()
    assert Path(LOG.file_path / 'log').resolve() == Path(
        LOG.file_path / '01-uiserver.log')


def test_init_log_with_established_setup(tmp_path):
    """Tests the entire logging init with a typically full logging dir"""
    LOG = RotatingUISFileHandler()
    LOG.file_path = Path(tmp_path/'.cylc'/'uiserver'/'log')
    LOG.file_path.mkdir(parents=True, exist_ok=True)
    for i in range(1, 5):
        file = (LOG.file_path / f'{i:02d}-uiserver.log')
        file.touch()
        file.write_text(f"This file started as: {file}")
    symlink_log = Path(LOG.file_path / 'log')
    symlink_log.symlink_to(LOG.file_path / f'01-uiserver.log')
    LOG.on_start()
    log_files = glob(os.path.join(LOG.file_path, f"*.log"))
    assert len(log_files) == 5
    actual_output = Path(LOG.file_path/'05-uiserver.log').read_text()
    expected_output = f"This file started as: {LOG.file_path}/04-uiserver.log"
    assert actual_output == expected_output
