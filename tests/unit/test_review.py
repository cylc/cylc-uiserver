# THIS FILE IS PART OF THE CYLC WORKFLOW ENGINE.
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

from io import BytesIO, StringIO
import pytest

from cylc.review.review import CylcReviewService


param = pytest.param


@pytest.fixture(scope='module')
def get_garbage_file(tmp_path_factory: pytest.TempdirFactory) -> str:
    """Create a file containing a byte which cannot be interpreted as UTF-8

    Check that attempting to read this file will lead to an error without
    extra handling.
    """
    fpath = tmp_path_factory.mktemp("temp") / 'garbage'
    fpath.write_bytes(b'\xe9')

    # Assert that the string is garbage if it's interpreted as utf-8:
    with pytest.raises(UnicodeDecodeError):
        fpath.read_text()

    return str(fpath)


def test_has_shebang_handle_contains_garbage():
    """Test is_shebang method for file handle input."""
    handle = BytesIO(b'\xe9')
    assert CylcReviewService._has_shebang(handle) is False


def test_has_shebang_handle_is_true():
    """It recognizes shebangs in text and binary files."""
    handle = StringIO('!#HelloWorld')
    assert CylcReviewService._has_shebang(handle) is True
    handle = BytesIO(b'!#HelloWorld')
    assert CylcReviewService._has_shebang(handle) is True


def test_has_shebang_file_bin_bad(get_garbage_file):
    """Test is_shebang method for file path input.

    Additionally, test a case where there is a non-utf-8 char at the
    start of the file.
    """
    assert CylcReviewService._has_shebang(get_garbage_file) is False


def test_get_file_text_nasty(get_garbage_file):
    """_get_file_text replaces non UTF-8 chars with question marks."""
    res = CylcReviewService()._get_file_text(get_garbage_file)
    assert res == '�'


@pytest.mark.parametrize(
    'workflows, sorted_names',
    (
        param(
            [
                {'name': 'A', 'last_activity_time': None},
                {'name': 'Z', 'last_activity_time': None}
            ],
            ['A', 'Z'],
            id='no-activity'
        ),
        param(
            [
                {'name': 'A', 'last_activity_time': None},
                {'name': 'Z', 'last_activity_time': '20'}
            ],
            ['Z', 'A'],
            id='some-active'
        ),
        param(
            [
                {'name': 'A', 'last_activity_time': '30'},
                {'name': 'Z', 'last_activity_time': '20'}
            ],
            ['A', 'Z'],
            id='both-active'
        ),
    )
)
def test_sort_workflows(workflows, sorted_names):
    """Workflow object sorting"""
    assert [
        w['name'] for w in CylcReviewService.sort_workflows(workflows)
    ] == sorted_names

def test_sort_workflows_plausible():
    """Case based on tests/function/cylc-review/08-suite-page.t
    Which was failing in CI
    """
    workflows = [
        {
            'name': '08-suites-page-2-2',
            'last_activity_time': '2026-03-27T11:23:31Z',
        },
        {
            'name': '08-suites-page-2-3',
            'last_activity_time': '2026-03-27T11:23:36Z',
        },
        {
            'name': '08-suites-page-2-1',
            'last_activity_time': '2026-03-27T11:23:27Z',
        },
    ]
    assert [
        i['name'] for i in CylcReviewService.sort_workflows(workflows)
    ] == [
        '08-suites-page-2-3',
        '08-suites-page-2-2',
        '08-suites-page-2-1',
    ]
