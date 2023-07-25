import asyncio
from async_timeout import timeout
import logging
import pytest
from unittest import mock

from cylc.flow import CYLC_LOG
from cylc.flow.id import Tokens
from cylc.flow.scripts.clean import CleanOptions
from cylc.uiserver.resolvers import (
    ENOENT_MSG,
    _schema_opts_to_api_opts,
    Services,
    process_cat_log_stderr,
)

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
        (services._return, 'Hello.', [True, 'Hello.']),
        (services._error, 'Goodbye.', [False, 'Goodbye.'])
    ]
)
def test_Services_anciliary_methods(func, message, expect):
    """Small functions return [bool, message].
    """
    assert func(message) == expect


async def test_cat_log(workflow_run_dir):
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
    expected = log_file.read_text()
    info = mock.MagicMock()
    info.root_value = 2
    # mock the context
    info.context = {'sub_statuses': {2: "start"}}
    workflow = Tokens(id_)
    log = logging.getLogger(CYLC_LOG)
    # note - timeout tests that the cat-log process is being stopped correctly

    first_response = None
    async with timeout(10):
        ret = services.cat_log(workflow, log, info)
        actual = ''
        is_first = True
        async for response in ret:
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
    assert actual.rstrip() == expected.rstrip()


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
