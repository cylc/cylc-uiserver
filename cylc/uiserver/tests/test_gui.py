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

import builtins
from glob import glob
import os
from pathlib import Path
import pytest
from random import randint
import requests
from shutil import rmtree
from time import sleep

from cylc.uiserver.scripts.gui import (
    get_url_from_file,
    select_info_file,
    update_url
)

@pytest.mark.parametrize(
    'existing_content,workflow_id,expected_updated_content',
    [
        pytest.param(
            'http://localhost:8892/cylc/?token=1234567890some_big_long_token1234567890#',
            None,
            'http://localhost:8892/cylc/?token=1234567890some_big_long_token1234567890#',
            id='existing_no_workflow_new_no_workflow'
        ),
        pytest.param(
            'http://localhost:8892/cylc/?token=1234567890some_big_long_token1234567890#',
            'some/workflow',
            'http://localhost:8892/cylc/?token=1234567890some_big_long_token1234567890#/workspace/some/workflow',
            id='existing_no_workflow_new_workflow'
        ),
        pytest.param(
            'http://localhost:8892/cylc/?token=1234567890some_big_long_token1234567890#/workspace/some/workflow',
            'another/flow',
            'http://localhost:8892/cylc/?token=1234567890some_big_long_token1234567890#/workspace/another/flow',
            id='existing_workflow_new_workflow'
        ),
        pytest.param(
            'http://localhost:8892/cylc/?token=1234567890some_big_long_token1234567890#/workspace/some/workflow',
            None,
            'http://localhost:8892/cylc/?token=1234567890some_big_long_token1234567890#',
            id='existing_workflow_no_new_workflow'
        ),
        pytest.param(
            '',
            'another/flow',
            None,
            id='no_url_no_change'
        ),
    ]
)
def test_update_html_file_updates_gui_file(
    existing_content,
    workflow_id,
        expected_updated_content):
    """Tests url is updated correctly"""

    updated_file_content = update_url(existing_content, workflow_id)
    assert updated_file_content == expected_updated_content


@pytest.mark.parametrize(
    'file_content,expected_url',
    [
        pytest.param(
            'content="1;url=http://localhost:8892/cylc/?token=1234567890some_big_long_token1234567890#/workspace/some/workflow" /> ',
            "http://localhost:8892/cylc/?token=1234567890some_big_long_token1234567890#/workspace/some/workflow",
            id='url_in_file'
        ),
        pytest.param(
            'There is no url in here',
            None,
            id='no_url_in_file'
        ),
    ]
)
def test_get_url_from_file(file_content, expected_url, tmp_path):
    Path(tmp_path).mkdir(exist_ok=True)
    tmp_gui_file = Path(tmp_path / "gui")
    tmp_gui_file.touch()
    tmp_gui_file.write_text(file_content)
    actual_url = get_url_from_file(tmp_gui_file)
    assert actual_url == expected_url


def test_gui_selection_and_clean_process(tmp_path, monkeypatch):
    """Testing functionally the gui selection and cleaning process"""
    # set up file structure
    info_files_dir = Path(tmp_path/'.cylc'/'uiserver'/'info_files')
    info_files_dir.mkdir(parents=True, exist_ok=True)
    for i in range(1, 5):
        pid = randint(1000, 100000)
        html_file = (info_files_dir / f"jpserver-{pid}-open.html")
        # the json file is unused but created empty to ensure the html is the
        # file used for selection
        json_file = (info_files_dir / f"jpserver-{pid}.json")
        json_file.touch()
        html_file.touch()
        html_file.write_text(f"content=\"1;url=http://localhost:8892/cylc/?token=1234567890some_big_long_token{pid}#/workspace/some/workflow\" more content")
        # Sleep ensure different modification time for sort
        sleep(0.1)
    mock_existing_guis = glob(os.path.join(info_files_dir, "*open.html"))
    monkeypatch.setattr(requests, 'get', mock_get)
    url = select_info_file(mock_existing_guis)
    # Test that the most recent ui-server is selected:
    assert url == f"http://localhost:8892/cylc/?token=1234567890some_big_long_token{pid}#/workspace/some/workflow"


def test_cleaning_of_info_files(tmp_path, monkeypatch):
    """Functionally tests the cleaning logic of the info files"""
    mock_info_files_dir = Path(tmp_path/'.cylc'/'uiserver'/'info_files')
    mock_info_files_dir.mkdir(parents=True, exist_ok=True)
    html_file = (mock_info_files_dir / f"jpserver-12345-open.html")
    json_file = (mock_info_files_dir / f"jpserver-12345.json")
    json_file.touch()
    html_file.touch()
    html_file.write_text(f"Some content but no url in here")
    assert html_file.exists() is True
    assert json_file.exists() is True
    # assert is called
    mock_existing_guis = glob(os.path.join(mock_info_files_dir, "*open.html"))
    monkeypatch.setattr(builtins, 'input', lambda *args, **kwargs: 'n')
    # test that a no user response keeps the files
    url = select_info_file(mock_existing_guis)
    assert url is None
    assert html_file.exists() is True
    assert json_file.exists() is True
    # Change user response to a yes and test files are removed
    monkeypatch.setattr(builtins, 'input', lambda *args, **kwargs: 'y')
    monkeypatch.setattr(
        'cylc.uiserver.scripts.gui.INFO_FILES_DIR',
        mock_info_files_dir
    )
    url = select_info_file(mock_existing_guis)
    assert url is None
    # test clean takes place
    assert html_file.exists() is False
    assert json_file.exists() is False


class MockResponse:
    """Used for the response of mocked request"""
    def __init__(self):
        self.status_code = 200


def mock_get(*args, **kwargs):
    return MockResponse()
