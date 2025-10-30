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

import asyncio
from concurrent.futures import ThreadPoolExecutor
import re
from typing import Any, Dict, List, Tuple
import logging
import os
import pytest
from unittest.mock import MagicMock, Mock
from subprocess import Popen, TimeoutExpired
from types import SimpleNamespace

from cylc.flow import CYLC_LOG
from cylc.flow.exceptions import CylcError
from cylc.flow.id import Tokens
from cylc.flow.scripts.clean import CleanOptions
from cylc.uiserver.resolvers import (
    ENOENT_MSG,
    _schema_opts_to_api_opts,
    Services,
    process_cat_log_stderr,
)
from cylc.uiserver.workflows_mgr import WorkflowsManager

services = Services()


@pytest.mark.parametrize(
    'schema_opts, schema, expect',
    [
        ({'rm': ''}, CleanOptions, {'rm_dirs': None}),
        ({'rm': 'work:share'}, CleanOptions, {'rm_dirs': ['work:share']}),
        ({'local_only': True}, CleanOptions, {'local_only': True}),
        ({'remote_only': False}, CleanOptions, {'remote_only': False}),
        ({'verbosity': 1}, CleanOptions, {'verbosity': 1}),
    ]
)
def test__schema_opts_to_api_opts(schema_opts, schema, expect):
    """It converts items correctly.
    """
    result = _schema_opts_to_api_opts(schema_opts, schema)
    assert schema(**expect) == result


@pytest.mark.parametrize(
    'func, message, expect',
    [
        (services._return, 'Hello.', (True, 'Hello.')),
        (services._error, 'Goodbye.', (False, 'Goodbye.'))
    ]
)
def test_Services_anciliary_methods(func, message, expect):
    """Small functions return [bool, message].
    """
    assert func(message) == expect


@pytest.mark.parametrize(
    'service', (Services.play, Services.validate_reinstall)
)
@pytest.mark.parametrize(
    'workflows, args, env, expected_ret, expected_env',
    [
        pytest.param(
            [Tokens('wflow1'), Tokens('~murray/wflow2')],
            {},
            {},
            (True, r"Workflow\(s\) .*ed"),
            {},
            id="multiple"
        ),
        pytest.param(
            [Tokens('~feynman/wflow1')],
            {},
            {},
            (False, "Cannot start workflows for other users."),
            {},
            id="other user's wflow"
        ),
        pytest.param(
            [Tokens('wflow1')],
            {'cylc_version': 'top'},
            {'CYLC_VERSION': 'bottom', 'CYLC_ENV_NAME': 'quark'},
            (True, r"Workflow\(s\) .*ed"),
            {'CYLC_VERSION': 'top'},
            id="cylc version overrides env"
        ),
        pytest.param(
            [Tokens('wflow1')],
            {},
            {'CYLC_VERSION': 'charm', 'CYLC_ENV_NAME': 'quark'},
            (True, r"Workflow\(s\) .*ed"),
            {'CYLC_VERSION': 'charm', 'CYLC_ENV_NAME': 'quark'},
            id="cylc env not overriden if no version specified"
        ),
    ]
)
async def test_start_services(
    service,
    monkeypatch: pytest.MonkeyPatch,
    workflows: List[Tokens],
    args: Dict[str, Any],
    env: Dict[str, str],
    expected_ret: list,
    expected_env: Dict[str, str],
):
    """It runs cylc play / vr correctly.

    Params:
        workflows: list of workflow tokens
        args: any args/options for cylc play
        env: any environment variables
        expected_ret: expected return value
        expected_env: any expected environment variables
    """
    monkeypatch.delenv('CYLC_ENV_NAME', raising=False)
    expected_env = {**os.environ, **expected_env}

    for k, v in env.items():
        monkeypatch.setenv(k, v)
    monkeypatch.setattr('cylc.uiserver.resolvers.getuser', lambda: 'murray')
    mock_popen = Mock(
        spec=Popen,
        return_value=Mock(
            spec=Popen,
            wait=Mock(return_value=0),
            communicate=lambda: ('out', 'err'),
        )
    )
    monkeypatch.setattr('cylc.uiserver.resolvers.Popen', mock_popen)

    status, message = await service(
        Mock(spec=WorkflowsManager),
        workflows,
        {'some': 'opt', **args},
        log=Mock(),
    )

    assert status == expected_ret[0]
    assert re.match(expected_ret[1], message)

    for i, call_args in enumerate(mock_popen.call_args_list):
        cmd_str = ' '.join(call_args.args[0])
        assert cmd_str.startswith('cylc ')
        assert '--some opt' in cmd_str
        assert workflows[i]['workflow'] in cmd_str

        assert call_args.kwargs['env'] == expected_env


@pytest.mark.parametrize(
    'service', (Services.play, Services.validate_reinstall)
)
@pytest.mark.parametrize(
    'workflows, popen_ret_codes, popen_communicate,'
    'expected_ret, expected_log',
    [
        pytest.param(
            [Tokens('wflow1')],
            [1],
            ("something", "bad things!!"),
            r"bad things!!.*",
            ["Command failed \(1\): cylc ", "something", "bad things!!"],
            id="one"
        ),
        pytest.param(
            [Tokens('wflow1'), Tokens('wflow2')],
            [1, 0],
            ("", "bad things!!"),
            r"\n\nwflow1: bad things!!\n\nwflow2: .*ed.*",
            [r"Command failed \(1\): cylc ", "bad things!!"],
            id="multiple"
        ),
        pytest.param(
            [Tokens('wflow1')],
            [1],
            ("something", ""),
            r"something.*",
            [r"Command failed \(1\): cylc ", "something"],
            id="uses stdout if stderr empty"
        ),
        pytest.param(
            [Tokens('wflow1')],
            [4],
            ("", ""),
            r"Command failed \(4\): cylc .*",
            [r"Command failed \(4\): cylc "],
            id="fallback msg if stdout/stderr empty"
        ),
    ]
)
async def test_start_services_fail(
    service,
    monkeypatch: pytest.MonkeyPatch,
    workflows: List[Tokens],
    popen_ret_codes: List[int],
    popen_communicate: Tuple[str, str],
    expected_ret: str,
    expected_log: List[str],
    caplog: pytest.LogCaptureFixture,
):
    """It returns suitable error messages if cylc play / vr fails.

    Params:
        workflows: list of workflow tokens
        popen_ret_codes: cylc play return codes for each workflow
        popen_communicate: stdout, stderr for cylc play
        expected: (beginning of) expected returned error message
    """
    popen_ret_codes = list(popen_ret_codes)
    mock_popen = Mock(
        spec=Popen,
        return_value=Mock(
            spec=Popen,
            wait=Mock(side_effect=lambda *a, **k: popen_ret_codes.pop(0)),
            communicate=Mock(return_value=popen_communicate),
        )
    )
    monkeypatch.setattr('cylc.uiserver.resolvers.Popen', mock_popen)
    caplog.set_level(logging.ERROR)

    status, message = await service(
        Mock(spec=WorkflowsManager),
        workflows,
        {},
        log=logging.root,
    )
    assert status is False
    assert re.match(expected_ret, message)

    # Should be logged too:
    for msg in expected_log:
        assert re.search(msg, caplog.text)


async def test_play_timeout(monkeypatch: pytest.MonkeyPatch):
    """It returns an error if cylc play times out."""
    def wait(timeout):
        raise TimeoutExpired('cylc play wflow1', timeout)

    mock_popen = Mock(
        spec=Popen,
        return_value=Mock(
            spec=Popen,
            wait=wait,
            communicate=lambda: ('out', 'err'),
        ),
    )
    monkeypatch.setattr('cylc.uiserver.resolvers.Popen', mock_popen)

    ret = await Services.play(
        Mock(spec=WorkflowsManager),
        [Tokens('wflow1')],
        {},
        log=Mock(),
    )
    assert ret == (
        False, "Command 'cylc play wflow1' timed out after 120 seconds\nerr"
    )


@pytest.fixture
def app():
    return SimpleNamespace(
        log=logging.getLogger(CYLC_LOG),
        log_timeout=10,
    )


@pytest.fixture
def fast_sleep(monkeypatch):
    monkeypatch.setattr(
        'cylc.uiserver.resolvers.Services.CAT_LOG_SLEEP',
        0.1,
    )


async def test_cat_log(workflow_run_dir, app, fast_sleep):
    """This is a functional test for cat_log subscription resolver.

    It creates a log file and then runs the cat_log service. Checking it
    returns all the logs. Note the log content should be over 20 lines to check
    the buffer logic.
    """
    (id_, log_dir) = workflow_run_dir
    log_file_content = """2022-11-08T11:10:05Z DEBUG - Starting
    2022-11-08T11:10:05Z DEBUG -
    2022-11-08T11:10:05Z DEBUG -
    2022-11-08T11:10:05Z DEBUG -
    2022-11-08T11:10:05Z DEBUG -
    2022-11-08T11:10:05Z DEBUG -
    2022-11-08T11:10:05Z DEBUG -
    2022-11-08T11:10:05Z INFO -
    2022-11-08T11:10:05Z INFO -
    2022-11-08T11:10:05Z INFO -
    2022-11-08T11:10:05Z INFO -
    2022-11-08T11:10:05Z INFO -
    2022-11-08T11:10:05Z INFO -
    2022-11-08T11:11:08Z DEBUG -
    2022-11-08T11:11:08Z INFO -
    2022-11-08T11:14:08Z WARNING -
    2022-11-08T11:14:08Z ERROR -
    2022-11-08T11:14:08Z WARNING -
    2022-11-08T11:14:09Z DEBUG -
    2022-11-08T11:14:09Z DEBUG -
    2022-11-08T11:14:11Z INFO - DONE
    """
    log_file = log_dir / '01-start-01.log'
    log_file.write_text(log_file_content)
    info = MagicMock()
    info.root_value = 2
    # mock the context
    info.context = {'sub_statuses': {2: "start"}}
    workflow = Tokens(id_)

    # note - timeout tests that the cat-log process is being stopped correctly
    first_response = None
    async with asyncio.timeout(20):
        ret = services.cat_log(workflow, app, info)
        actual = ''
        is_first = True
        async for response in ret:
            if err := response.get('error'):
                # Surface any unexpected errors for better visibility
                app.log.exception(err)
            if is_first:
                first_response = response
                is_first = False
            for line in response.get('lines', []):
                actual += line
                if "DONE" in line:
                    info.context['sub_statuses'][2] = 'stop'
            await asyncio.sleep(0)

    # the first response should include the log file path and
    # connection status
    assert first_response['path'].endswith('01-start-01.log')
    assert first_response['connected'] is True

    # the last response should change the connected status
    assert response['connected'] is False

    # the other responses should contain the log file lines
    assert actual.rstrip() == log_file_content.rstrip()


async def test_cat_log_timeout(workflow_run_dir, app, fast_sleep):
    """This is a functional test for cat_log subscription resolver.

    It creates a log file and then runs the cat_log service. Checking it
    returns all the logs. Note the log content should be over 20 lines to check
    the buffer logic.
    """
    (id_, log_dir) = workflow_run_dir
    log_file = log_dir / '01-start-01.log'
    log_file.write_text('forty two')
    info = MagicMock()
    info.root_value = 2
    # mock the context
    info.context = {'sub_statuses': {2: "start"}}
    workflow = Tokens(id_)

    app.log_timeout = 0

    ret = services.cat_log(workflow, app, info)
    responses = []
    async with asyncio.timeout(5):
        async for response in ret:
            responses.append(response)
            await asyncio.sleep(0)

    assert len(responses) == 1
    assert responses[0]['connected'] is False
    assert 'error' not in responses[0]


@pytest.mark.parametrize(
    'text, expected',
    [
        (b"", ""),
        (b"dog \n", "dog"),
        (f"tail: dog: {ENOENT_MSG}\ntail: no files remaining".encode(),
         ENOENT_MSG),
    ]
)
def test_process_cat_log_stderr(text: bytes, expected: str):
    assert process_cat_log_stderr(text) == expected


async def test_clean__error(
    monkeypatch: pytest.MonkeyPatch, caplog: pytest.LogCaptureFixture
):
    """It returns an error if the clean command fails."""
    def bad_clean(*a, **k):
        raise CylcError("bad things!!")

    monkeypatch.setattr('cylc.uiserver.resolvers._clean', bad_clean)
    caplog.set_level(logging.ERROR)

    ret = Services.clean(
        Mock(spec=WorkflowsManager),
        [Tokens('wflow1')],
        {},
        executor=ThreadPoolExecutor(1),
        log=logging.root,
    )
    err_msg = "CylcError: bad things!!"
    assert (await ret) == (False, err_msg)
    assert err_msg in caplog.text
