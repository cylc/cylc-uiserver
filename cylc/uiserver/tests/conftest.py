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
from getpass import getuser
import inspect
from pathlib import Path
from shutil import rmtree
from socket import gethostname
from tempfile import TemporaryDirectory
from textwrap import dedent

import pytest
import zmq

from cylc.flow.data_messages_pb2 import (  # type: ignore
    PbEntireWorkflow,
    PbWorkflow,
    PbFamilyProxy,
)
from cylc.flow.network import ZMQSocketBase

from cylc.uiserver.data_store_mgr import DataStoreMgr
from cylc.uiserver.main import CylcUIServer
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

    def stop(self, *args, **kwargs):
        pass


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
def uiserver() -> CylcUIServer:
    return CylcUIServer(0, '/mock', '')


@pytest.fixture
def make_entire_workflow():
    def _make_entire_workflow(workflow_id):
        workflow = PbWorkflow()
        workflow.id = workflow_id
        entire_workflow = PbEntireWorkflow()
        entire_workflow.workflow.CopyFrom(workflow)
        root_family = PbFamilyProxy()
        root_family.name = 'root'
        entire_workflow.family_proxies.extend([root_family])
        return entire_workflow

    return _make_entire_workflow


@pytest.fixture
def one_workflow_aiter():
    """An async generator fixture that returns a single workflow.
    """
    async def _create_aiter(*args, **kwargs):
        yield kwargs

    return _create_aiter


@pytest.fixture
def empty_aiter():
    """An async generator fixture that does not return anything."""
    class NoopIterator:

        def __aiter__(self):
            return self

        async def __anext__(self):
            raise StopAsyncIteration

    return NoopIterator


@pytest.fixture(scope='module')
def mod_tmp_path():
    """A tmp_path fixture with module-level scope."""
    path = Path(TemporaryDirectory().name)
    path.mkdir()
    yield path
    rmtree(path)


@pytest.fixture(scope='module')
def ui_build_dir(mod_tmp_path):
    """A dummy UI build tree containing three versions '1.0', '2.0' & '3.0'."""
    for version in range(1, 4):
        path = mod_tmp_path / f'{version}.0'
        path.mkdir()
        (path / 'index.html').touch()
    yield mod_tmp_path


@pytest.fixture
def mock_config(monkeypatch):
    """Mock the UIServer/Hub configuration file.

    This fixture auto-loads by setting a blank config.

    Call the fixture with config code to override.

    mock_config('''
        c.UIServer.my_config = 'my_value'
    ''')

    Can be called multiple times.

    Note the code you provide is exec'ed just like the real config file.

    """
    conf = ''

    def _write(string=''):
        nonlocal conf
        conf = dedent(string)

    def _read(obj, _):
        nonlocal conf
        exec(conf, {'c': obj.config})

    monkeypatch.setattr(
        'cylc.uiserver.main.CylcUIServer.load_config_file',
        _read
    )

    yield _write


@pytest.fixture
def authorisation_true(monkeypatch):
    """Disabled request authorisation for test purposes."""
    monkeypatch.setattr(
        'cylc.uiserver.',
        lambda x: True
    )


@pytest.fixture
def mock_authentication(monkeypatch):

    def _mock_authentication(user=None, server=None, none=False):
        ret = {
            'name': user or getuser(),
            'server': server or gethostname()
        }
        if none:
            ret = None
        monkeypatch.setattr(
            'cylc.uiserver.handlers.BaseHandler.get_current_user',
            lambda x: ret
        )

    _mock_authentication()

    return _mock_authentication


@pytest.fixture
def mock_authentication_yossarian(mock_authentication):
    mock_authentication(user='yossarian')


@pytest.fixture
def mock_authentication_none(mock_authentication):
    mock_authentication(none=True)
