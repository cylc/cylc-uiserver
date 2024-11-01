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

from cylc.uiserver.services.source_workflows import (
    _get_source_workflow_name,
    _get_workflow_source,
    list_source_workflows,
)

import pytest


@pytest.fixture(scope='module')
def source_dirs(mod_monkeypatch, mod_tmp_path):
    source_dir_a = mod_tmp_path / 'a'
    source_dir_b = mod_tmp_path / 'b'
    source_dir_a.mkdir()
    source_dir_b.mkdir()

    # a:foo
    foo = source_dir_a / 'foo'
    foo.mkdir()
    (foo / 'flow.cylc').touch()

    # a:bar/b1
    bar = source_dir_a / 'bar/b1'
    bar.mkdir(parents=True)
    (bar / 'flow.cylc').touch()

    # b:baz
    baz = source_dir_b / 'baz'
    baz.mkdir()
    (baz / 'flow.cylc').touch()

    mod_monkeypatch.setattr(
        'cylc.uiserver.services.source_workflows.SOURCE_DIRS',
        [source_dir_a, source_dir_b]
    )

    mod_monkeypatch.setattr(
        'cylc.uiserver.services.source_workflows.CWD',
        mod_tmp_path.absolute(),
    )

    return [source_dir_a, source_dir_b]


def _make_installed_workflow(mod_tmp_path, id_, source_path, run_name='run1'):
    root_run_dir = mod_tmp_path / id_
    if run_name:
        run_dir = root_run_dir / run_name
    else:
        run_dir = root_run_dir
    run_dir.mkdir(parents=True)
    (run_dir / 'flow.cylc').touch()
    if source_path:
        install_dir = (root_run_dir / '_cylc-install')
        install_dir.mkdir()
        (install_dir / 'source').symlink_to(source_path)
    return root_run_dir


@pytest.fixture(scope='module')
def installed_workflows(source_dirs, mod_monkeypatch, mod_tmp_path):
    a, b, *_ = source_dirs

    def _get_workflow_run_dir(id_):
        return mod_tmp_path / id_

    mod_monkeypatch.setattr(
        'cylc.uiserver.services.source_workflows.get_workflow_run_dir',
        _get_workflow_run_dir,
    )

    # ~user/foo/run1: normally installed workflow
    _make_installed_workflow(
        mod_tmp_path,
        'one', a / 'foo',
    )

    # ~user/bar: installed from source outside of SOURCE_DIRS
    _make_installed_workflow(
        mod_tmp_path,
        'two',
        mod_tmp_path / 'somewhere-else',
        run_name=None,
    )

    # ~user/baz: not installed
    _make_installed_workflow(
        mod_tmp_path,
        'three',
        None,
    )


def test_get_source_workflow_name(source_dirs):
    a, b, *_ = source_dirs
    assert _get_source_workflow_name(a / 'foo') == 'foo'
    assert _get_source_workflow_name(a / 'bar/b1') == 'bar/b1'
    assert _get_source_workflow_name(b / 'baz') == 'baz'


async def test_list_source_workflows(source_dirs):
    a, b, *_ = source_dirs
    source_workflows = await list_source_workflows()
    assert sorted(source_workflows, key=lambda x: x['name']) == [
        {
            'name': 'bar/b1',
            'path': a / 'bar/b1',
            'relative_path': Path('a/bar/b1'),
        },
        {
            'name': 'baz',
            'path': b / 'baz',
            'relative_path': Path('b/baz'),
        },
        {
            'name': 'foo',
            'path': a / 'foo',
            'relative_path': Path('a/foo'),
        },
    ]


def test_get_workflow_source(source_dirs, installed_workflows, monkeypatch, mod_tmp_path):
    a, b, *_ = source_dirs
    assert _get_workflow_source('one') == {
        'name': 'foo',
        'path': a / 'foo',
        'relative_path': Path('a/foo'),
    }
    assert _get_workflow_source('two') == {
        'name': None,
        'path': a.parent / 'somewhere-else',
        'relative_path': Path('somewhere-else'),
    }
    assert _get_workflow_source('three') == {
        'name': None,
        'path': None,
        'relative_path': None,
    }

    # test a workflow source that is not relative to CWD
    monkeypatch.setattr(
        'cylc.uiserver.services.source_workflows.CWD',
        mod_tmp_path.absolute() / 'x/y/z',
    )
    assert _get_workflow_source('one') == {
        'name': 'foo',
        'path': a / 'foo',
        'relative_path': None,  # <== not relative
    }
