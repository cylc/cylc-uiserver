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

from getpass import getuser
from itertools import product
import logging
from random import random
import socket

import pytest
from pytest_mock import MockFixture

from cylc.flow import ID_DELIM
from cylc.flow.exceptions import ClientError, ClientTimeout
from cylc.flow.network import API
from cylc.flow.suite_files import (
    SuiteFiles,
    ContactFileFields as CFF,
)

from cylc.uiserver.main import CylcUIServer
import cylc.uiserver.workflows_mgr as workflows_mgr_module
from cylc.uiserver.workflows_mgr import (
    workflow_request,
    WorkflowsManager,
    est_workflow,
)

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
    mocked_get_host_ip_by_name.side_effect = lambda x: 'remote_host' \
        if x == 'remote' else x

    r_reg, r_host, r_port, r_pub_port, r_client, r_result = await est_workflow(
        reg, host, port, pub_port, timeout)
    assert reg == r_reg
    assert expected_host == r_host
    assert port == r_port
    assert pub_port == r_pub_port
    assert r_client.__class__ == AsyncClientFixture


# --- WorkflowsManager


def test_workflows_manager_spawn_workflow(workflows_manager):
    workflows_manager.spawn_workflow()
    assert not workflows_manager.active

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
    # generate all possible state changes
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

    # the flow should be marked as becoming inactive then active again
    assert [change[:3] for change in changes] == [
        (wid, 'active', 'inactive'),
        (wid, 'inactive', 'active')
    ]

    # it should have picked up the new uuid too
    assert changes[1][3][CFF.UUID] == '42'


@pytest.mark.asyncio
async def test_multi_request(
        workflows_manager, async_client: AsyncClientFixture):
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

    workflows_manager.active[workflow_id] = {
        'req_client': async_client
    }

    response = await workflows_manager.multi_request(
        '', [workflow_id], None, multi_args)
    assert 1 == len(response)
    assert value == response[0]


@pytest.mark.asyncio
async def test_multi_request_gather_errors(
        workflows_manager, async_client: AsyncClientFixture,
        mocker: MockFixture):
    workflow_id = 'gather-error-workflow'
    error_type = ValueError
    async_client.will_return(error_type)

    workflows_manager.active[workflow_id] = {
        'req_client': async_client
    }

    logger = logging.getLogger(workflows_mgr_module.__name__)
    mocked_exception_function = mocker.patch.object(logger, 'exception')
    await workflows_manager.multi_request('', [workflow_id], None, None)
    mocked_exception_function.assert_called_once()
    assert mocked_exception_function.call_args[1][
               'exc_info'].__class__ == error_type


@pytest.mark.asyncio
async def test_register(
        uiserver: CylcUIServer,
        mocker: MockFixture,
        one_workflow_aiter
):
    """Test the registration of a workflow.

    It depends on the pipes returning a workflow with no
    previous state, and the next state as 'active'."""
    workflow_name = 'register-me'
    workflow_id = f'{getuser()}|{workflow_name}'

    assert workflow_id not in uiserver.data_store_mgr.data
    assert workflow_id not in uiserver.workflows_mgr.active

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
    # NOTE: here we will yield a workflow that is running, it has contact
    #       data, is not active nor inactive (i.e. pending registration).
    #       This is what forces the .update() to call register()!

    # We don't have a real workflow, so we mock get_location.
    mocker.patch(
        'cylc.flow.network.client.get_location',
        return_value=('localhost', 0, None)
    )
    # The following functions also depend on a running workflow
    # with pyzmq socket, so we also mock them.
    mocker.patch('cylc.flow.network.client.SuiteRuntimeClient.start')
    mocker.patch('cylc.flow.network.client.SuiteRuntimeClient.get_header')
    mocker.patch('cylc.uiserver.data_store_mgr.DataStoreMgr.'
                 'start_subscription')

    await uiserver.workflows_mgr.update()

    # register must have created an entry in the workflow manager
    assert workflow_id in uiserver.workflows_mgr.active


@pytest.mark.asyncio
async def test_unregister(
        uiserver: CylcUIServer,
        one_workflow_aiter,
        empty_aiter
):
    """A workflow, once registered, can be unregistered in the
    workflow manager.

    It will delegate to the data store to properly remove the
    workflow from the data store attributes, and call the necessary
    functions."""
    workflow_name = 'unregister-me'

    uiserver.workflows_mgr._scan_pipe = empty_aiter()
    uiserver.workflows_mgr.inactive.add(workflow_name)
    # NOTE: here we will yield a workflow that is not running, it does
    #       not have the contact data and is inactive.
    #       This is what forces the .update() to call unregister()!

    await uiserver.workflows_mgr.update()

    # now the workflow is not active, nor inactive, it is unregistered
    assert workflow_name not in uiserver.workflows_mgr.inactive


@pytest.mark.asyncio
async def test_connect(
        uiserver: CylcUIServer,
        mocker: MockFixture,
        one_workflow_aiter
):
    """Test connecting to a workflow.

    If a workflow is running, but in the inactive state,
    then the connect method will be called."""
    workflow_name = 'connect'
    workflow_id = f'{getuser()}|{workflow_name}'
    uiserver.workflows_mgr.inactive.add(workflow_id)

    assert workflow_id not in uiserver.workflows_mgr.active
    assert workflow_id in uiserver.workflows_mgr.inactive

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
    # NOTE: here we will yield a workflow that is running, it has contact
    #       data, is not active nor inactive (i.e. pending registration).
    #       This is what forces the .update() to call register()!

    # We don't have a real workflow, so we mock get_location.
    mocker.patch(
        'cylc.flow.network.client.get_location',
        return_value=('localhost', 0, None)
    )
    # The following functions also depend on a running workflow
    # with pyzmq socket, so we also mock them.
    mocker.patch('cylc.flow.network.client.SuiteRuntimeClient.start')
    mocker.patch('cylc.flow.network.client.SuiteRuntimeClient.get_header')
    mocker.patch('cylc.uiserver.data_store_mgr.DataStoreMgr.'
                 'start_subscription')

    async def my_sync_workflow(*args, **kwargs):
        return True
    mocker.patch(
        'cylc.uiserver.data_store_mgr.DataStoreMgr.sync_workflow',
        side_effect=my_sync_workflow
    )

    await uiserver.workflows_mgr.update()

    # connect must have created an active entry for the workflow,
    # and the update method must have taken care to remove from inactive
    assert workflow_id in uiserver.workflows_mgr.active
    assert not uiserver.workflows_mgr.inactive


@pytest.mark.asyncio
async def test_disconnect_and_stop(
        uiserver: CylcUIServer,
        mocker: MockFixture,
        one_workflow_aiter,
        async_client: AsyncClientFixture
):
    """Test disconnecting and stopping a workflow.

    If a workflow is active, but the next state is inactive, the
    workflow manager will take care to stop and disconnect the workflow."""
    workflow_name = 'disconnect-stop'
    workflow_id = f'{getuser()}|{workflow_name}'

    flow = {
            'name': workflow_name,
            'contact': False,
            CFF.HOST: 'localhost',
            CFF.PORT: 0,
            CFF.PUBLISH_PORT: 0,
            CFF.API: 1,
            'req_client': async_client
        }
    uiserver.workflows_mgr.active[workflow_id] = flow

    assert workflow_id not in uiserver.workflows_mgr.inactive
    assert workflow_id in uiserver.workflows_mgr.active

    uiserver.workflows_mgr._scan_pipe = one_workflow_aiter(
        **flow
    )
    # NOTE: here we will yield a workflow that is running, it has contact
    #       data, is not active nor inactive (i.e. pending registration).
    #       This is what forces the .update() to call register()!

    # We don't have a real workflow, so we mock get_location.
    mocker.patch(
        'cylc.flow.network.client.get_location',
        return_value=('localhost', 0, None)
    )
    # The following functions also depend on a running workflow
    # with pyzmq socket, so we also mock them.
    mocker.patch('cylc.flow.network.client.SuiteRuntimeClient.start')
    mocker.patch('cylc.flow.network.client.SuiteRuntimeClient.get_header')
    mocker.patch('cylc.uiserver.data_store_mgr.DataStoreMgr.'
                 'start_subscription')
    mocker.patch('cylc.uiserver.data_store_mgr.DataStoreMgr.update_contact')

    await uiserver.workflows_mgr.update()

    # connect must have created an active entry for the workflow,
    # and the update method must have taken care to remove from inactive
    assert workflow_id not in uiserver.workflows_mgr.active
    assert workflow_id in uiserver.workflows_mgr.inactive

# TODO: add tests for remaining methods in WorkflowsManager
