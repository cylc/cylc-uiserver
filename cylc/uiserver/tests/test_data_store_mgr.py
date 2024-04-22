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
    entire_workflow = make_entire_workflow(w_id)
    async_client.will_return(entire_workflow.SerializeToString())

    # Set the client used by our test workflow.
    data_store_mgr.workflows_mgr.workflows[w_id] = {
        'req_client': async_client
    }

    # Call the entire_workflow_update function.
    # This should use the client defined above (``async_client``) when
    # calling ``workflow_request``.
    await data_store_mgr._entire_workflow_update(w_id)

    # The ``DataStoreMgr`` sets the workflow data retrieved in its
    # own ``.data`` dictionary, which will contain Protobuf message
    # objects.
    w_id_data = data_store_mgr.data[w_id]

    # If everything went OK, we should have the Protobuf object
    # de-serialized and added to the ``DataStoreMgr.data``
    # (the workflow ID is its key).
    assert entire_workflow.workflow.id == w_id_data['workflow'].id


async def test_connect_workflow_error(
    monkeypatch,
    data_store_mgr,
    caplog,
):
    """It should catch and log errors.

    The _start_subscription and _entire_workflow_update methods will attempt
    connect to and communicate with workflows, this could result in errors e.g.
    WorkflowStopped or ClientTimeout.

    The "connect_workflow" method should catch and log these errors.
    """
    # mock a workflow for the data store to pretend to connect to
    w_id = 'myflow'
    contact_data = {
        'name': w_id,
        CFF.HOST: 'meh',
        CFF.PUBLISH_PORT: '123',
    }

    # an arbitrary exception to raise
    exc = Exception(f'such and such error: {w_id}')

    # mock the data store methods so this error is raised
    async def _raise_client_error(*args):
        raise exc

    monkeypatch.setattr(
        data_store_mgr,
        '_start_subscription',
        _raise_client_error
    )
    monkeypatch.setattr(
        data_store_mgr,
        '_entire_workflow_update',
        _raise_client_error
    )

    caplog.set_level(0)
    caplog.clear()

    # attempt to connect
    await data_store_mgr.connect_workflow(w_id, contact_data)

    # ensure the error is logged
    assert caplog.record_tuples == [
        (
            'cylc',
            20,
            f"[data-store] connect_workflow('{w_id}', <dict>)",
        ),
        (
            'cylc',
            40,
            f'Failed to connect to myflow: such and such error: {w_id}',
        ),
        (
            'cylc',
            20,
            f"[data-store] disconnect_workflow('{w_id}')",
        ),
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
