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

from itertools import product
import logging
from random import random
from typing import Type

import pytest

from cylc.flow.id import Tokens
from cylc.flow.exceptions import ClientError, ClientTimeout
from cylc.flow.network import API
from cylc.flow.workflow_files import (
    WorkflowFiles,
    ContactFileFields as CFF,
)

from cylc.uiserver.app import CylcUIServer
from cylc.uiserver.workflows_mgr import (
    workflow_request,
    WorkflowsManager,
)

from .conftest import AsyncClientFixture

LOG = logging.getLogger('cylc')


# --- workflow_request

@pytest.mark.parametrize(
    'exc', [ClientError, ClientTimeout]
)
async def test_workflow_request_client_error(
    exc: Type[Exception],
    async_client: AsyncClientFixture,
    caplog: pytest.LogCaptureFixture
):
    caplog.set_level(logging.ERROR, logger='cylc')
    logger = logging.getLogger('cylc')
    async_client.will_return(exc)
    with pytest.raises(exc):
        await workflow_request(client=async_client, command='', log=logger)
    assert exc.__name__ in caplog.text


async def test_workflow_request(async_client: AsyncClientFixture):
    """Test normal response of workflow_request matches async_request"""
    async_client.will_return(42)
    res = await workflow_request(client=async_client, command='')
    assert res == 42


# --- WorkflowsManager


def mk_flow(path, reg, active=True, database=True):
    """Make a workflow appear on the filesystem for scan purposes.

    Args:
        path (pathlib.Path):
            The directory to create the mocked workflow in.
        reg (str):
            The registered name for this workflow.
        active (bool):
            If True then a contact file will be written.

    """
    run_dir = path / reg
    srv_dir = run_dir / WorkflowFiles.Service.DIRNAME
    contact = srv_dir / WorkflowFiles.Service.CONTACT
    database_path = srv_dir / WorkflowFiles.Service.DB
    fconfig = run_dir / WorkflowFiles.FLOW_FILE
    run_dir.mkdir()
    fconfig.touch()  # cylc uses this to identify a dir as a workflow
    srv_dir.mkdir()
    if database:
        database_path.touch()
    if active:
        with open(contact, 'w+') as contact_file:
            contact_file.write(
                '\n'.join([
                    f'{CFF.API}={API}',
                    f'{CFF.HOST}=42',
                    f'{CFF.PORT}=42',
                    f'{CFF.NAME}=42',
                    f'{CFF.UUID}=42'
                ])
            )


@pytest.mark.parametrize(
    # generate all possible normal state changes
    'active_before,active_after',
    product(['active', 'inactive', None], repeat=2)
)
async def test_workflow_state_changes(tmp_path, active_before, active_after):
    """It correctly identifies workflow state changes from the filesystem."""
    tmp_path /= str(random())
    tmp_path.mkdir()

    # mock the results of the previous scan
    wfm = WorkflowsManager(None, LOG, context=None, run_dir=tmp_path)
    wid = Tokens(user=wfm.owner, workflow='a').id

    ret = (
        {wid} if active_before == 'active' else set(),
        {wid} if active_before == 'inactive' else set(),
    )
    wfm.get_workflows = lambda: ret

    # mock the filesystem in the new state
    if active_after == 'active':
        mk_flow(tmp_path, 'a', active=True)
    if active_after == 'inactive':
        mk_flow(tmp_path, 'a', active=False)

    # see what state changes the workflow manager detects
    changes = []
    async for change in wfm._workflow_state_changes():
        changes.append(change)

    # compare those changes to expectations
    if active_before == active_after:
        assert changes == []
    else:
        assert len(changes) == 1
        assert (wid, active_before, active_after) == changes[0][:3]


@pytest.mark.parametrize(
    'active_before,active_after',
    product([True, False], repeat=2)
)
async def test_workflow_state_change_uuid(
    tmp_path,
    active_before,
    active_after
):
    """It identifies discontinuities in workflow runs.

    A workflow run is defined by its UUID. If this changes the workflow manager
    must detect the change and re-register the workflow because any data known
    about the workflow is now out of date.

    This can happen because:

    * A workflow was deleted and installed between scans.
    * The user deleted the workflow database.

    """
    # mock the result of the previous scan
    wfm = WorkflowsManager(None, LOG, context=None, run_dir=tmp_path)
    wid = Tokens(user=wfm.owner, workflow='a').id

    wfm.workflows[wid] = {
        CFF.API: API,
        CFF.UUID: '41'
    }

    if active_before:
        wfm.get_workflows = lambda: ({wid}, set())
    else:
        wfm.get_workflows = lambda: (set(), {wid})

    if active_after:
        # create a workflow with the same name but a different UUID
        # (simulates a new workflow run being started)
        mk_flow(tmp_path, 'a', active=True)
    else:
        # create a workflow without a database
        # (simulates the database being removed or workflow re-created)
        mk_flow(tmp_path, 'a', active=False, database=False)

    # see what state changes the workflow manager detects
    changes = []
    async for change in wfm._workflow_state_changes():
        changes.append(change)

    # the flow should be marked as becoming inactive then active again
    assert [change[:3] for change in changes] == [
        (
            wid,
            ('/active' if active_before else '/inactive'),
            ('active' if active_after else 'inactive'),
        )
    ]

    # it should have picked up the new uuid too
    if active_after:
        assert changes[0][3][CFF.UUID] == '42'


async def test_multi_request(
    workflows_manager: WorkflowsManager,
    async_client: AsyncClientFixture
):
    workflow_id = 'multi-request-workflow'
    # The response for a workflow multi-request.
    value = 42
    res = {
        workflow_id: {
            'result': [
                value
            ]
        }
    }
    async_client.will_return(res)
    multi_args = {
        workflow_id: None
    }

    workflows_manager.workflows[workflow_id] = {
        'req_client': async_client
    }

    response = await workflows_manager.multi_request(
        '', [workflow_id], None, multi_args)
    assert len(response) == 1
    assert response[0] == res


async def test_multi_request_gather_errors(
    workflows_manager,
    async_client: AsyncClientFixture,
    caplog: pytest.LogCaptureFixture
):
    workflow_id = 'gather-error-workflow'
    error_type = ValueError
    async_client.will_return(error_type)
    async_client.workflow = workflow_id

    workflows_manager.workflows[workflow_id] = {
        'req_client': async_client
    }

    caplog.clear()
    await workflows_manager.multi_request('', [workflow_id], None, None)
    assert caplog.record_tuples == [
        ('cylc', 40, f'Error communicating with {workflow_id}'),
        ('cylc', 40, 'x'),
    ]
    exc_info = caplog.records[1].exc_info
    assert exc_info and exc_info[0] == error_type


async def test_crashed_workflow(one_workflow_aiter, caplog, uis_caplog):
    """It should swallow client connect errors."""
    # create a UIS, configure it for logging
    uiserver = CylcUIServer()
    uis_caplog(caplog, uiserver, logging.DEBUG)
    caplog.clear()

    # register a running workflow, the UIS will attempt to connect to it ...
    uiserver.workflows_mgr._scan_pipe = one_workflow_aiter(**{
        'name': 'workflow-does-not-exist',
        'contact': True,
        CFF.HOST: 'localhost',
        CFF.PORT: 0,
        CFF.PUBLISH_PORT: 0,
        CFF.API: 1,
    })

    # ... connection will fail, the UIS should catch the ClientError
    await uiserver.workflows_mgr.update()

    # we should have two log messages
    assert len(caplog.records) == 2
    # one when it attempted to register the workflow
    assert 'register_workflow' in caplog.records[0].message
    # and one when it failed to connect
    assert 'Could not connect' in caplog.records[1].message
