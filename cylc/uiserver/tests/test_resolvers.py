import pytest
from unittest import mock

from cylc.flow.scripts.clean import CleanOptions
from cylc.uiserver.resolvers import (
    _schema_opts_to_api_opts,
    Services
)
from pathlib import Path

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


@mock.patch("build_cmd")
def test_cat_log(tmp_path, mocked_build_cmd):
    Path(tmp_path).mkdir(exist_ok=True)
    tmp_log_file = (tmp_path / 'log').touch()
    log_file_content = """
    2022-11-08T11:10:05Z DEBUG - Starting
    2022-11-08T11:10:05Z DEBUG - auth received API command b'CURVE'
    2022-11-08T11:10:05Z DEBUG - Processing with Jinja2
    2022-11-08T11:10:05Z DEBUG - Expanding [runtime] namespace lists and parameters
    2022-11-08T11:10:05Z DEBUG - Parsing the runtime namespace hierarchy
    2022-11-08T11:10:05Z DEBUG - Parsing [special tasks]
    2022-11-08T11:10:05Z DEBUG - Parsing the dependency graph
    2022-11-08T11:10:05Z INFO - Run: (re)start number=1, log rollover=1
    2022-11-08T11:10:05Z INFO - Cylc version: 8.0.4.dev
    2022-11-08T11:10:05Z INFO - Run mode: live
    2022-11-08T11:10:05Z INFO - Initial point: 20200202T0202Z
    2022-11-08T11:10:05Z INFO - Final point: 20200202T0202Z
    2022-11-08T11:10:05Z INFO - Cold start from 20200202T0202Z
    2022-11-08T11:11:08Z DEBUG - PT3M inactivity timer starts NOW
    2022-11-08T11:11:08Z INFO - [20200202T0202Z/t1 succeeded job:03 flows:1] (polled)succeeded at 2022-11-08T11:11:04Z
    2022-11-08T11:14:08Z WARNING - inactivity timer timed out after PT3M
    2022-11-08T11:14:08Z ERROR - Workflow shutting down - "abort on inactivity timeout" is set
    2022-11-08T11:14:08Z WARNING - Orphaned task jobs:
        * 20200202T0202Z/t2 (submitted)
    2022-11-08T11:14:09Z DEBUG - stopping zmq replier...
    2022-11-08T11:14:09Z DEBUG - ...stopped
    2022-11-08T11:14:09Z DEBUG - stopping zmq publisher...
    2022-11-08T11:14:09Z DEBUG - ...stopped
    2022-11-08T11:14:09Z DEBUG - auth received API command b'TERMINATE'
    2022-11-08T11:14:09Z DEBUG - Removing authentication keys from scheduler
    2022-11-08T11:14:11Z INFO - DONE"""
    tmp_log_file.write(log_file_content)
    mocked_build_cmd.return_value = ['tail', "-f", tmp_log_file]
    info = mock.MagicMock()
    ret = services.Services.cat_log('workflow',info)
    assert ret == "blah"
    print("mel!")
