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
from cylc.flow.network import MSG_TIMEOUT
from cylc.flow.suite_files import ContactFileFields as CFF

import cylc.uiserver.data_store_mgr as data_store_mgr_module
from cylc.uiserver.data_store_mgr import DataStoreMgr
from .conftest import AsyncClientFixture


@pytest.mark.asyncio
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
    data_store_mgr.workflows_mgr.active[w_id] = {
        'req_client': async_client
    }

    # Call the entire_workflow_update function.
    # This should use the client defined above (``async_client``) when
    # calling ``workflow_request``.
    await data_store_mgr.entire_workflow_update()

    # The ``DataStoreMgr`` sets the workflow data retrieved in its
    # own ``.data`` dictionary, which will contain Protobuf message
    # objects.
    w_id_data = data_store_mgr.data[w_id]

    # If everything went OK, we should have the Protobuf object
    # de-serialized and added to the ``DataStoreMgr.data``
    # (the workflow ID is its key).
    assert entire_workflow.workflow.id == w_id_data['workflow'].id


@pytest.mark.asyncio
async def test_entire_workflow_update_ignores_timeout_message(
        async_client: AsyncClientFixture,
        data_store_mgr: DataStoreMgr
):
    """
    Test that ``entire_workflow_update`` ignores if the client
    receives a ``MSG_TIMEOUT`` message.
    """
    w_id = 'workflow_id'
    async_client.will_return(MSG_TIMEOUT)

    # Set the client used by our test workflow.
    data_store_mgr.workflows_mgr.active[w_id] = {
        'req_client': async_client
    }

    # Call the entire_workflow_update function.
    # This should use the client defined above (``async_client``) when
    # calling ``workflow_request``.
    await data_store_mgr.entire_workflow_update()

    # When a ``MSG_TIMEOUT`` happens, the ``DataStoreMgr`` object ignores
    # that message. So it means that its ``.data`` dictionary MUST NOT
    # have an entry for the Workflow ID.
    assert w_id not in data_store_mgr.data


@pytest.mark.asyncio
async def test_entire_workflow_update_gather_error(
        async_client: AsyncClientFixture,
        data_store_mgr: DataStoreMgr,
        mocker
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
    error_type = ValueError
    async_client.will_return(error_type)

    # Set the client used by our test workflow.
    data_store_mgr.workflows_mgr.active['workflow_id'] = {
        'req_client': async_client
    }

    # Call the entire_workflow_update function.
    # This should use the client defined above (``async_client``) when
    # calling ``workflow_request``.
    logger = logging.getLogger(data_store_mgr_module.__name__)
    mocked_exception_function = mocker.patch.object(logger, 'exception')
    await data_store_mgr.entire_workflow_update()
    mocked_exception_function.assert_called_once()
    assert mocked_exception_function.call_args[1][
               'exc_info'].__class__ == error_type


@pytest.mark.asyncio
async def test_register_workflow(
    data_store_mgr: DataStoreMgr
):
    """Passing a workflow ID through register_workflow creates
    an entry for the workflow in the data store .data map, and another
    entry in the data store .delta_queues map."""
    w_id = 'user|workflow_id'
    await data_store_mgr.register_workflow(w_id=w_id)
    assert w_id in data_store_mgr.data
    assert w_id in data_store_mgr.delta_queues


@pytest.mark.asyncio
async def test_update_contact_no_contact_data(
    data_store_mgr: DataStoreMgr
):
    """Updating contact with no contact data results in default values
    for the workflow in the data store, like the API version set to zero."""
    w_id = 'user|workflow_id'
    api_version = 0
    await data_store_mgr.register_workflow(w_id=w_id)
    data_store_mgr.update_contact(w_id=w_id, contact_data=None)
    assert api_version == data_store_mgr.data[w_id]['workflow'].api_version


@pytest.mark.asyncio
async def test_update_contact_with_contact_data(
    data_store_mgr: DataStoreMgr
):
    """Updating contact with contact data sets the values int he data store
    for the workflow."""
    w_id = 'user|workflow_id'
    api_version = 1
    await data_store_mgr.register_workflow(w_id=w_id)
    contact_data = {
        'name': 'workflow_id',
        'owner': 'cylc',
        CFF.HOST: 'localhost',
        CFF.PORT: 40000,
        CFF.API: api_version
    }
    data_store_mgr.update_contact(w_id=w_id, contact_data=contact_data)
    assert api_version == data_store_mgr.data[w_id]['workflow'].api_version


@pytest.mark.asyncio
async def test_stop_workflow(
    data_store_mgr: DataStoreMgr
):
    """Telling a data store to stop a workflow, is the same as updating
    contact with no contact data."""
    w_id = 'user|workflow_id'
    api_version = 1
    await data_store_mgr.register_workflow(w_id=w_id)
    contact_data = {
        'name': 'workflow_id',
        'owner': 'cylc',
        CFF.HOST: 'localhost',
        CFF.PORT: 40000,
        CFF.API: api_version
    }
    data_store_mgr.update_contact(w_id=w_id, contact_data=contact_data)
    assert api_version == data_store_mgr.data[w_id]['workflow'].api_version

    data_store_mgr.stop_workflow(w_id=w_id)
    assert 0 == data_store_mgr.data[w_id]['workflow'].api_version
