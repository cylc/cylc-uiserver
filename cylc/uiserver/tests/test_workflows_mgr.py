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

import pytest

from pytest_mock import MockFixture

from cylc.uiserver.workflows_mgr import *
from cylc.flow.exceptions import ClientTimeout

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
async def test_workflow_request_client_error(async_client: AsyncClientFixture):
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


def test_workflows_manager_constructor():
    mgr = WorkflowsManager(None)
    assert not mgr.workflows


def test_workflows_manager_spawn_workflow():
    mgr = WorkflowsManager(None)
    mgr.spawn_workflow()
    assert not mgr.workflows

# TODO: add tests for remaining methods in WorkflowsManager
