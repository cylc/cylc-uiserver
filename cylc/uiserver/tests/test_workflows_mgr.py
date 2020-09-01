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
from pathlib import Path
import pytest
from random import random

from pytest_mock import MockFixture

from cylc.flow import ID_DELIM
from cylc.flow.exceptions import ClientTimeout
from cylc.flow.network import API
from cylc.flow.suite_files import (
    ContactFileFields as CFF,
    SuiteFiles
)

from cylc.uiserver.workflows_mgr import *

from .conftest import AsyncClientFixture


# --- workflow_request

@pytest.mark.asyncio
async def test_workflow_request_client_timeout(
        async_client: AsyncClientFixture):
    async_client.will_return(ClientTimeout)
    ctx, msg = await workflow_request(client=async_client, command='')
    assert not ctx
    assert 'timeout' in msg.lower()


@pytest.mark.asyncio
async def test_workflow_request_client_error(
        async_client: AsyncClientFixture, caplog):
    caplog.set_level(logging.CRITICAL, logger='cylc')
    async_client.will_return(ClientError)
    ctx, msg = await workflow_request(client=async_client, command='')
    assert not ctx
    assert not msg


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "returns,command,req_context,expected_ctx,expected_msg",
    [
        pytest.param(
            42, 'cmd', None, 'cmd', 42
        ),
        pytest.param(
            42, '', None, '', 42
        ),
        pytest.param(
            42, 'cmd', 'some-context', 'some-context', 42
        )
    ])
async def test_workflow_request(
        async_client: AsyncClientFixture,
        returns,
        command,
        req_context,
        expected_ctx,
        expected_msg
):
    async_client.will_return(returns)
    ctx, msg = await workflow_request(
        client=async_client, command=command, req_context=req_context)
    assert expected_ctx == ctx
    assert expected_msg == msg


# --- est_workflow


@pytest.mark.asyncio
async def test_est_workflow_socket_error(
    mocker: MockFixture,
):
    mocked_is_remote_host = mocker.patch(
        'cylc.uiserver.workflows_mgr.is_remote_host')
    mocked_is_remote_host.return_value = True

    mocked_get_host_ip_by_name = mocker.patch(
        'cylc.uiserver.workflows_mgr.get_host_ip_by_name')

    def side_effect(*_, **__):
        raise socket.error
    mocked_get_host_ip_by_name.side_effect = side_effect
    reg, host, port, pub_port, client = await est_workflow(
        '', '', 0, 0)
    assert not any([reg, host, port, pub_port, client])
    assert client is None


@pytest.mark.asyncio
@pytest.mark.parametrize('reg,host,port,pub_port,timeout,expected_host', [
        pytest.param(
            'remote', 'remote', 8000, 8002, 1, 'remote_host'
        ),
        pytest.param(
            'local', 'localhost', 4000, 4001, 2, 'localhost'
        )
    ])
async def test_est_workflow(
        async_client: AsyncClientFixture,
        mocker: MockFixture,
        reg,
        host,
        port,
        pub_port,
        timeout,
        expected_host
):
    mocked_is_remote_host = mocker.patch(
        'cylc.uiserver.workflows_mgr.is_remote_host')
    mocked_is_remote_host.side_effect = lambda x: True \
        if x == 'remote' else False

    mocked_client = mocker.patch(
        'cylc.uiserver.workflows_mgr.SuiteRuntimeClient')
    mocked_client.return_value = async_client

    mocked_get_host_ip_by_name = mocker.patch(
        'cylc.uiserver.workflows_mgr.get_host_ip_by_name')
    mocked_get_host_ip_by_name.side_effect = lambda x: f'remote_host' \
        if x == 'remote' else x

    r_reg, r_host, r_port, r_pub_port, r_client, r_result = await est_workflow(
        reg, host, port, pub_port, timeout)
    assert reg == r_reg
    assert expected_host == r_host
    assert port == r_port
    assert pub_port == r_pub_port
    assert r_client.__class__ == AsyncClientFixture


# --- WorkflowsManager


def test_workflows_manager_spawn_workflow():
    mgr = WorkflowsManager(None)
    mgr.spawn_workflow()
    assert not mgr.active

# TODO: add tests for remaining methods in WorkflowsManager


def mk_flow(path, reg, active=True):
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
    srv_dir = run_dir / SuiteFiles.Service.DIRNAME
    contact = srv_dir / SuiteFiles.Service.CONTACT
    fconfig = run_dir / SuiteFiles.FLOW_FILE
    run_dir.mkdir()
    fconfig.touch()  # cylc uses this to identify a dir as a workflow
    srv_dir.mkdir()
    if active:
        with open(contact, 'w+') as contact_file:
            contact_file.write(
                '\n'.join([
                    f'{CFF.API}={API}',
                    f'{CFF.HOST}=42',
                    f'{CFF.PORT}=42',
                    f'{CFF.UUID}=42'
                ])
            )


@pytest.mark.asyncio
@pytest.mark.parametrize(
    # generate all possile state changes
    'active_before,active_after',
    product(['active', 'inactive', None], repeat=2)
)
async def test_workflow_state_changes(tmp_path, active_before, active_after):
    """It correctly identifies workflow state changes from the filesystem."""
    tmp_path /= str(random())
    tmp_path.mkdir()

    # mock the results of the previous scan
    wfm = WorkflowsManager(None, context=None, run_dir=tmp_path)
    wid = f'{wfm.owner}{ID_DELIM}a'
    if active_before == 'active':
        wfm.active[wid] = {
            CFF.API: API,
            CFF.UUID: '42'
        }
    elif active_before == 'inactive':
        wfm.inactive.add(wid)

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


@pytest.mark.asyncio
async def test_workflow_state_change_restart(tmp_path):
    """It identifies workflows which have restarted between scans."""
    # mock the result of the previous scan
    wfm = WorkflowsManager(None, context=None, run_dir=tmp_path)
    wid = f'{wfm.owner}{ID_DELIM}a'
    wfm.active[wid] = {
            CFF.API: API,
            CFF.UUID: '41'
    }

    # create a new workflow with the same name but a different UUID
    mk_flow(tmp_path, 'a', active=True)

    # see what state changes the workflow manager detects
    changes = []
    async for change in wfm._workflow_state_changes():
        changes.append(change)

    # the flow should be marked as becomming inactive then active again
    assert [change[:3] for change in changes] == [
        (wid, 'active', 'inactive'),
        (wid, 'inactive', 'active')
    ]

    # it should have picked up the new uuid too
    assert changes[1][3][CFF.UUID] == '42'
