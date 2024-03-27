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

from getpass import getuser
import inspect
import logging
from pathlib import Path
from shutil import rmtree
from socket import gethostname
from tempfile import TemporaryDirectory
from uuid import uuid4

import pytest
from tornado.web import HTTPError
from traitlets.config import Config
import zmq

from jupyter_server.auth.identity import User

from cylc.flow.cfgspec.glbl_cfg import glbl_cfg
from cylc.flow.id import Tokens
from cylc.flow.data_messages_pb2 import (  # type: ignore
    PbEntireWorkflow,
    PbWorkflow,
    PbFamilyProxy,
)
from cylc.flow.network.client import WorkflowRuntimeClient
from cylc.flow.workflow_files import ContactFileFields as CFF

from cylc.uiserver.data_store_mgr import DataStoreMgr
from cylc.uiserver.workflows_mgr import WorkflowsManager


class AsyncClientFixture(WorkflowRuntimeClient):
    pattern = zmq.REQ
    host = ''
    port = 0
    workflow = 'myflow'

    def __init__(self):
        self.returns = None

    def will_return(self, returns):
        self.returns = returns

    async def async_request(
        self, command, args=None, timeout=None, req_meta=None
    ):
        if isinstance(self.returns, Exception):
            raise self.returns
        if (
            inspect.isclass(self.returns)
            and issubclass(self.returns, Exception)
        ):
            raise self.returns('x')
        return self.returns

    def stop(self, *args, **kwargs):
        pass


@pytest.fixture
def async_client():
    return AsyncClientFixture()


@pytest.fixture
def workflows_manager() -> WorkflowsManager:
    return WorkflowsManager(None, logging.getLogger('cylc'))


@pytest.fixture
def data_store_mgr(workflows_manager: WorkflowsManager) -> DataStoreMgr:
    return DataStoreMgr(
        workflows_mgr=workflows_manager,
        log=logging.getLogger('cylc')
    )


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
    async def _create_aiter(*args, none=False, **kwargs):
        if none:
            return
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
    """Mock the UIServer/Hub configuration.

    This fixture auto-loads by setting a blank config.

    Call the fixture with config code to override.

    mock_config(
        CylcUIServer={
            'trait': 42
        }
    )

    Can be called multiple times.

    """
    conf = {}

    def _write(**kwargs):
        nonlocal conf
        conf = kwargs

    def _read(self):
        nonlocal conf
        self.config = Config(conf)

    monkeypatch.setattr(
        'cylc.uiserver.app.CylcUIServer.initialize_settings',
        _read
    )

    yield _write


@pytest.fixture
def authorisation_true(monkeypatch):
    """Disabled request authorisation for test purposes."""
    monkeypatch.setattr(
        'cylc.uiserver.handlers._authorise',
        lambda x: True
    )


@pytest.fixture
def authorisation_false(monkeypatch):
    """Disabled request authorisation for test purposes."""
    monkeypatch.setattr(
        'cylc.uiserver.handlers._authorise',
        lambda x: False
    )


@pytest.fixture
def mock_authentication_yossarian(monkeypatch):
    user = User('yossarian')
    monkeypatch.setattr(
        'cylc.uiserver.handlers.CylcAppHandler.current_user',
        user,
    )
    monkeypatch.setattr(
        'cylc.uiserver.handlers.is_bearer_token_authenticated',
        lambda x: True,
    )


@pytest.fixture
def jp_server_config(jp_template_dir):
    """Config to turn the CylcUIServer extension on.

    Auto-loading, add as an argument in the test function to activate.
    """
    config = {
        "ServerApp": {
            "jpserver_extensions": {
                'cylc.uiserver': True
            },
        }
    }
    return config


@pytest.fixture
def patch_conf_files(monkeypatch):
    """Auto-patches the CylcUIServer to prevent it loading config files.

    Auto-loading, add as an argument in the test function to activate.
    """
    monkeypatch.setattr(
        'cylc.uiserver.app.CylcUIServer.config_file_paths', []
    )


@pytest.fixture
def cylc_uis(jp_serverapp):
    """Return the UIS extension for the JupyterServer ServerApp."""
    return [
        *jp_serverapp.extension_manager.extension_apps['cylc.uiserver']
    ][0]


@pytest.fixture
def cylc_workflows_mgr(cylc_uis):
    """Return the workflows manager for the UIS extension."""
    return cylc_uis.workflows_mgr


@pytest.fixture
def cylc_data_store_mgr(cylc_uis):
    """Return the data store manager for the UIS extension."""
    return cylc_uis.data_store_mgr


@pytest.fixture
def disable_workflows_update(cylc_workflows_mgr, monkeypatch):
    """Prevent the workflow manager from scanning for workflows.

    Auto-loading, add as an argument in the test function to activate.
    """
    monkeypatch.setattr(cylc_workflows_mgr, 'update', lambda: None)


@pytest.fixture
def disable_workflow_connection(cylc_data_store_mgr, monkeypatch):
    """Prevent the data store manager from connecting to workflows.

    Auto-loading, add as an argument in the test function to activate.
    """

    async def _null(*args, **kwargs):
        pass

    monkeypatch.setattr(
        cylc_data_store_mgr,
        'connect_workflow',
        _null
    )


@pytest.fixture
def dummy_workflow(
    cylc_workflows_mgr,
    disable_workflow_connection,
    disable_workflows_update,
    monkeypatch,
):
    """Register a dummy workflow with the workflow manager / data store.

    Use like so:

      dummy_workflow('id')

    Workflows registered in this way will appear as stopped but will contain
    contact info as if they were running (change this later as required).

    No connection will be made to the schedulers (because they don't exist).

    """

    async def _register(name):
        await cylc_workflows_mgr._register(
            Tokens(user='me', workflow=name).id,
            {
                'name': name,
                'owner': 'me',
                CFF.HOST: 'localhost',
                CFF.PORT: 1234,
                CFF.API: 1,
            },
            True,
        )

    return _register


@pytest.fixture
def uis_caplog():
    """Patch the UIS logging to allow caplog to do its job.

    Use like so:
        uiserver = CylcUIServer()
        uis_caplog(caplog, uiserver, logging.<level>)
        # continue using caplog as normal

    See test_fixtures for example.

    """
    def _caplog(caplog, uiserver, level=logging.INFO):
        uiserver.log.handlers = [caplog.handler]
        caplog.set_level(level, uiserver.log.name)

    return _caplog


@pytest.fixture(scope='session')
def port_range():
    return glbl_cfg().get(['scheduler', 'run hosts', 'ports'])


@pytest.fixture()
def workflow_run_dir(request):
    "Set up workflow run dir, with log_dirs"
    flow_name = f'cylctb-uiserver-{str(uuid4())[:8]}'
    run_dir = Path('~/cylc-run' / Path(flow_name)).expanduser().resolve()
    run_dir.mkdir(parents=True, exist_ok=True)
    log_dir = Path(run_dir / 'log' / 'scheduler')
    log_dir.mkdir(parents=True, exist_ok=True)
    yield flow_name, log_dir
    if not request.session.testsfailed:
        rmtree(run_dir)
