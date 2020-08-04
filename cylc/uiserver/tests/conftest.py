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
"""Test code and fixtures."""

import asyncio
import inspect

import pytest
import zmq
from cylc.flow.data_messages_pb2 import PbEntireWorkflow, PbWorkflow
from cylc.flow.network import ZMQSocketBase

from cylc.uiserver.data_store_mgr import DataStoreMgr
from cylc.uiserver.workflows_mgr import WorkflowsManager


class AsyncClientFixture(ZMQSocketBase):
    pattern = zmq.REQ
    host = ''
    port = 0

    def __init__(self):
        self.returns = None

    def will_return(self, returns):
        self.returns = returns

    async def async_request(self, command, args=None, timeout=None):
        if inspect.isclass(self.returns) and \
                issubclass(self.returns, Exception):
            raise self.returns
        return self.returns


@pytest.fixture
def async_client():
    return AsyncClientFixture()


@pytest.fixture
def event_loop():
    """This fixture defines the event loop used for each test."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    # gracefully exit async generators
    loop.run_until_complete(loop.shutdown_asyncgens())
    # cancel any tasks still running in this event loop
    for task in asyncio.all_tasks(loop):
        task.cancel()
    loop.close()


@pytest.fixture
def workflows_manager() -> WorkflowsManager:
    return WorkflowsManager(None)


@pytest.fixture
def data_store_mgr(workflows_manager: WorkflowsManager) -> DataStoreMgr:
    return DataStoreMgr(workflows_mgr=workflows_manager)


@pytest.fixture
def make_entire_workflow():
    def _make_entire_workflow(workflow_id):
        workflow = PbWorkflow()
        workflow.id = workflow_id
        entire_workflow = PbEntireWorkflow()
        entire_workflow.workflow.CopyFrom(workflow)
        return entire_workflow

    return _make_entire_workflow
