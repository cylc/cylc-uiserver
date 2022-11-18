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

from functools import partial
from getpass import getuser
import logging
from types import SimpleNamespace

import pytest

from cylc.flow.id import Tokens
from cylc.flow.workflow_files import ContactFileFields as CFF

from cylc.uiserver.workflows_mgr import WorkflowsManager

"""Test interaction between the workflows manager and data store."""


def dummy_uis():
    calls = []

    async def async_capture(func, *_):
        nonlocal calls
        calls.append(func)

    def sync_capture(func, *_):
        nonlocal calls
        calls.append(func)

    data_store_mgr = SimpleNamespace(
        register_workflow=partial(async_capture, 'register'),
        unregister_workflow=partial(async_capture, 'unregister'),
        connect_workflow=partial(async_capture, 'connect'),
        disconnect_workflow=partial(sync_capture, 'disconnect'),
        calls=calls,
    )

    uis = SimpleNamespace(data_store_mgr=data_store_mgr)
    wfm = WorkflowsManager(uis, logging.getLogger())
    uis.workflows_mgr = wfm

    return uis


@pytest.mark.parametrize(
    'before,after,actions',
    [
        (
            None,
            None,
            [],
        ),
        (
            None,
            'inactive',
            ['register'],
        ),
        (
            None,
            'active',
            ['register', 'connect'],
        ),
        (
            'inactive',
            None,
            ['unregister'],
        ),
        (
            'inactive',
            'inactive',
            [],
        ),
        (
            'inactive',
            'active',
            ['connect'],
        ),
        (
            'active',
            None,
            ['disconnect', 'unregister'],
        ),
        (
            'active',
            'inactive',
            ['disconnect'],
        ),
        (
            'active',
            'active',
            [],
        ),
    ],
)
async def test_data_store_changes(
    one_workflow_aiter,
    monkeypatch,
    before,
    after,
    actions,
):
    monkeypatch.setattr(
        'cylc.uiserver.workflows_mgr.WorkflowRuntimeClient',
        lambda *a, **k: True
    )

    workflow_name = 'register-me'
    wid = Tokens(user=getuser(), workflow=workflow_name).id
    uiserver = dummy_uis()

    # mock the state of the data store
    ret = [
        {wid} if before == 'active' else set(),
        {wid} if before == 'inactive' else set(),
    ]
    uiserver.data_store_mgr.get_workflows = lambda: ret

    # mock the scan result
    if after == 'active':
        uiserver.workflows_mgr._scan_pipe = one_workflow_aiter(
            **{
                'name': workflow_name,
                'contact': True,
                CFF.HOST: 'localhost',
                CFF.PORT: 0,
                CFF.PUBLISH_PORT: 0,
                CFF.API: 1
            }
        )
    elif after == 'inactive':
        uiserver.workflows_mgr._scan_pipe = one_workflow_aiter(
            **{
                'name': workflow_name,
                'contact': False,
            }
        )
    else:
        uiserver.workflows_mgr._scan_pipe = one_workflow_aiter(none=True)

    # run the update
    await uiserver.workflows_mgr.update()

    # see which data store methods got hit
    assert uiserver.data_store_mgr.calls == actions
