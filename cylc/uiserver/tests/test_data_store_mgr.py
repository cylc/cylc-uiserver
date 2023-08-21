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

"""Tests for the ``data_store_mgr`` module and its objects and functions."""

import logging

import pytest
import zmq

from cylc.flow.exceptions import ClientTimeout, WorkflowStopped
from cylc.flow.id import Tokens
from cylc.flow.network import ZMQSocketBase
from cylc.flow.workflow_files import ContactFileFields as CFF

from cylc.uiserver.data_store_mgr import DataStoreMgr

from .conftest import AsyncClientFixture


async def test_entire_workflow_update(
    async_client: AsyncClientFixture,
    data_store_mgr: DataStoreMgr,
    make_entire_workflow
):
    """Test that ``entire_workflow_update`` is executed successfully."""
    w_id = 'workflow_id'
    entire_workflow = make_entire_workflow(f'{w_id}')
    async_client.will_return(entire_workflow.SerializeToString())

    # Set the client used by our test workflow.
    data_store_mgr.workflows_mgr.workflows[w_id] = {
        'req_client': async_client
    }

    # Call the entire_workflow_update function.
    # This should use the client defined above (``async_client``) when
    # calling ``workflow_request``.
    await data_store_mgr._entire_workflow_update()

    # The ``DataStoreMgr`` sets the workflow data retrieved in its
    # own ``.data`` dictionary, which will contain Protobuf message
    # objects.
    w_id_data = data_store_mgr.data[w_id]

    # If everything went OK, we should have the Protobuf object
    # de-serialized and added to the ``DataStoreMgr.data``
    # (the workflow ID is its key).
    assert entire_workflow.workflow.id == w_id_data['workflow'].id


async def test_entire_workflow_update_ignores_timeout_message(
    async_client: AsyncClientFixture,
    data_store_mgr: DataStoreMgr
):
    """
    Test that ``entire_workflow_update`` ignores if the client
    receives a ``MSG_TIMEOUT`` message.
    """
    w_id = 'workflow_id'
    async_client.will_return(ClientTimeout)

    # Set the client used by our test workflow.
    data_store_mgr.workflows_mgr.workflows[w_id] = {
        'req_client': async_client
    }

    # Call the entire_workflow_update function.
    # This should use the client defined above (``async_client``) when
    # calling ``workflow_request``.
    await data_store_mgr._entire_workflow_update()

    # When a ClientTimeout happens, the ``DataStoreMgr`` object ignores
    # that message. So it means that its ``.data`` dictionary MUST NOT
    # have an entry for the Workflow ID.
    assert w_id not in data_store_mgr.data


async def test_entire_workflow_update_gather_error(
    async_client: AsyncClientFixture,
    data_store_mgr: DataStoreMgr,
    caplog: pytest.LogCaptureFixture,
):
    """
    Test that if ``asyncio.gather`` in ``entire_workflow_update``
    has a coroutine raising an error, it will handle the error correctly.
    """
    # The ``AsyncClient`` will raise an error. This will happen when
    # ``workflow_request`` is called via ``asyncio.gather``, which
    # would be raised if ``return_exceptions`` is not given.
    #
    # This test wants to confirm this is not raised, but instead the
    # error is returned, so that we can inspect, log, etc.
    async_client.will_return(ValueError)

    # Set the client used by our test workflow.
    data_store_mgr.workflows_mgr.workflows['workflow_id'] = {
        'req_client': async_client
    }

    # Call the entire_workflow_update function.
    # This should use the client defined above (``async_client``) when
    # calling ``workflow_request``.
    await data_store_mgr._entire_workflow_update()
    assert caplog.record_tuples == [
        ('cylc', 40, 'Error communicating with myflow'),
        ('cylc', 40, 'x'),
        ('cylc', 40,
         'Failed to update entire local data-store of a workflow: x'),
    ]
    exc_info = caplog.records[1].exc_info
    assert exc_info and exc_info[0] == ValueError


async def test_entire_workflow_update__stopped_workflow(
    async_client: AsyncClientFixture,
    data_store_mgr: DataStoreMgr,
    caplog: pytest.LogCaptureFixture,
):
    """Test that DataStoreMgr._entire_workflow_update() handles a stopped
    workflow reasonably."""
    exc = WorkflowStopped('myflow')
    async_client.will_return(exc)
    data_store_mgr.workflows_mgr.workflows['workflow_id'] = {
        'req_client': async_client
    }
    await data_store_mgr._entire_workflow_update()
    assert caplog.record_tuples == [
        ('cylc', 40, f'WorkflowStopped: {exc}'),
    ]


async def test_register_workflow(
    data_store_mgr: DataStoreMgr
):
    """Passing a workflow ID through register_workflow creates
    an entry for the workflow in the data store .data map, and another
    entry in the data store .delta_queues map."""
    w_id = Tokens(user='user', workflow='workflow_id').id
    await data_store_mgr.register_workflow(w_id=w_id, is_active=False)
    assert w_id in data_store_mgr.data
    assert w_id in data_store_mgr.delta_queues


async def test_update_contact_no_contact_data(
    data_store_mgr: DataStoreMgr
):
    """Updating contact with no contact data results in default values
    for the workflow in the data store, like the API version set to zero."""
    w_id = Tokens(user='user', workflow='workflow_id').id
    api_version = 0
    await data_store_mgr.register_workflow(w_id=w_id, is_active=False)
    assert data_store_mgr._update_contact(w_id=w_id, contact_data=None)
    assert api_version == data_store_mgr.data[w_id]['workflow'].api_version


async def test_update_contact_no_workflow(
    data_store_mgr: DataStoreMgr
):
    """Ensure _update_contact doesn't error if the workflow is missing.

    This can happen if the workflow is removed.
    """
    assert not data_store_mgr._update_contact(w_id='elephant')


async def test_update_contact_with_contact_data(
    data_store_mgr: DataStoreMgr
):
    """Updating contact with contact data sets the values int he data store
    for the workflow."""
    w_id = Tokens(user='user', workflow='workflow_id').id
    api_version = 1
    await data_store_mgr.register_workflow(w_id=w_id, is_active=False)
    contact_data = {
        'name': 'workflow_id',
        'owner': 'cylc',
        CFF.HOST: 'localhost',
        CFF.PORT: 40000,
        CFF.API: api_version
    }
    data_store_mgr._update_contact(w_id=w_id, contact_data=contact_data)
    assert api_version == data_store_mgr.data[w_id]['workflow'].api_version


async def test_disconnect_workflow(
    data_store_mgr: DataStoreMgr
):
    """Telling a data store to stop a workflow, is the same as updating
    contact with no contact data."""
    w_id = Tokens(user='user', workflow='workflow_id').id
    api_version = 1
    await data_store_mgr.register_workflow(w_id=w_id, is_active=False)
    contact_data = {
        'name': 'workflow_id',
        'owner': 'cylc',
        CFF.HOST: 'localhost',
        CFF.PORT: 40000,
        CFF.API: api_version
    }
    data_store_mgr._update_contact(
        w_id=w_id,
        contact_data=contact_data,
        status='Something'
    )
    assert api_version == data_store_mgr.data[w_id]['workflow'].api_version

    data_store_mgr.disconnect_workflow(w_id=w_id)
    assert data_store_mgr.data[w_id]['workflow'].api_version == 0


async def test_workflow_connect_fail(
    data_store_mgr: DataStoreMgr,
    port_range,
    monkeypatch,
    caplog,
):
    """Simulate a failure during workflow connection.

    The data store should "rollback" any incidental changes made during the
    failed connection attempt by disconnecting from the workflow afterwards.

    Not an ideal test as we don't actually get a communication failure,
    the data store manager just skips contacting the workflow because
    we aren't providing a client for it to connect to, however, probably the
    best we can achieve without actually running a workflow.
    """
    # patch the zmq logic so that the connection doesn't fail at the first
    # hurdle
    monkeypatch.setattr(
        'cylc.flow.network.ZMQSocketBase._socket_bind', lambda *a, **k: None,
    )

    # start a ZMQ REPLY socket in order to claim an unused port
    w_id = Tokens(user='user', workflow='workflow_id').id
    try:
        context = zmq.Context()
        server = ZMQSocketBase(
            zmq.REP,
            context=context,
            workflow=w_id,
            bind=True,
        )
        server._socket_bind(*port_range)

        # register the workflow with the data store
        await data_store_mgr.register_workflow(w_id=w_id, is_active=False)
        contact_data = {
            'name': 'workflow_id',
            'owner': 'cylc',
            CFF.HOST: 'localhost',
            CFF.PORT: server.port,
            CFF.PUBLISH_PORT: server.port,
            CFF.API: 1
        }

        # try to connect to the workflow
        caplog.set_level(logging.DEBUG, data_store_mgr.log.name)
        await data_store_mgr.connect_workflow(w_id, contact_data)

        # the connection should fail because our ZMQ socket is not a
        # WorkflowRuntimeServer with the correct endpoints and auth
        assert [record.message for record in caplog.records] == [
            "[data-store] connect_workflow('~user/workflow_id', <dict>)",
            'failed to connect to ~user/workflow_id',
            "[data-store] disconnect_workflow('~user/workflow_id')",
        ]
    finally:
        # tidy up
        server.stop()
        context.destroy()
