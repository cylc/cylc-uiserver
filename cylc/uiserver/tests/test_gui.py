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

import json
from pathlib import Path
import pytest
import os

from cylc.uiserver.scripts.gui import update_html_file

@pytest.mark.parametrize(
    'existing_content,workflow_id,expected_updated_content',
    [
        pytest.param(
            'content="1;url=http://localhost:8892/cylc/?token=1234567890some_big_long_token1234567890#" /> ',
            None,
            'content="1;url=http://localhost:8892/cylc/?token=1234567890some_big_long_token1234567890#" /> ',
            id='existing_no_workflow_new_no_workflow'
        ),
        pytest.param(
            'content="1;url=http://localhost:8892/cylc/?token=1234567890some_big_long_token1234567890#" /> ',
            'some/workflow',
            'content="1;url=http://localhost:8892/cylc/?token=1234567890some_big_long_token1234567890#/workflows/some/workflow" /> ',
            id='existing_no_workflow_new_workflow'
        ),
        pytest.param(
            'content="1;url=http://localhost:8892/cylc/?token=1234567890some_big_long_token1234567890#/workflows/some/workflow" /> ',
            'another/flow',
            'content="1;url=http://localhost:8892/cylc/?token=1234567890some_big_long_token1234567890#/workflows/another/flow" /> ',
            id='existing_workflow_new_workflow'
        ),
        pytest.param(
            'content="1;url=http://localhost:8892/cylc/?token=1234567890some_big_long_token1234567890#/workflows/some/workflow" /> ',
            None,
            'content="1;url=http://localhost:8892/cylc/?token=1234567890some_big_long_token1234567890#" /> ',
            id='existing_workflow_no_new_workflow'
        ),
        pytest.param(
            'content="1;no url in this file "',
            'another/flow',
            'content="1;no url in this file "',
            id='no_url_no_change'
        ),
    ]
)
def test_update_html_file_updates_gui_file(
    existing_content,
    workflow_id,
    expected_updated_content,
    tmp_path):
    """Tests html file is updated correctly"""
    Path(tmp_path).mkdir(exist_ok=True)
    tmp_gui_file = Path(tmp_path / "gui")
    tmp_gui_file.touch()
    tmp_gui_file.write_text(existing_content)
    update_html_file(tmp_gui_file, workflow_id)
    updated_file_content = tmp_gui_file.read_text()

    assert updated_file_content == expected_updated_content
