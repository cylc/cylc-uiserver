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

from pathlib import Path
import pytest
import os

from cylc.uiserver.scripts.gui import check_pid


def test_check_pid_raises_error_for_existing_process(mod_tmp_path):
    """Tests exisiting process in file raises Exception"""
    pid = os.getpid()
    tmp_pid_file = Path(mod_tmp_path/"pid")
    with open(tmp_pid_file, "w") as f:
        f.write(str(pid))
    with pytest.raises(Exception) as exc_msg:
        check_pid(tmp_pid_file)
    assert f'cylc gui is running at process id: {pid}' == str(exc_msg.value)


def test_checking_no_pid_file_does_not_raise_exception(mod_tmp_path):
    """Test check with no process id file runs without exception."""
    tmp_pid_file = Path(mod_tmp_path)
    try:
        check_pid(tmp_pid_file)
    except Exception as ex:
        pytest.fail(f"check_pid() raised Exception unexpectedly: {ex}")


def test_check_junk_in_pid_file_deletes_file(mod_tmp_path):
    """Tests exisiting process in file raises Exception"""
    tmp_pid_file = Path(mod_tmp_path/"pid")
    with open(tmp_pid_file, "w") as f:
        f.write(str("This is a load of rubbish."))
    check_pid(tmp_pid_file)
    assert not tmp_pid_file.exists()
