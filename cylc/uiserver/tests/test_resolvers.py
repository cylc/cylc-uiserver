import pytest
from os import getpid
from types import SimpleNamespace

from cylc.uiserver.resolvers import (
    _schema_opts_to_api_opts,
    InvalidSchemaOptionError,
    clean,
    Services
)


services = Services()


@pytest.mark.parametrize(
    'schema_opts, expect',
    [
        ({'rm': ''}, {'rm_dirs': ''}),
        ({'rm': 'work share'}, {'rm_dirs': 'work share'}),
        ({'local_only': True}, {'local_only': True}),
        ({'remote_only': False}, {'remote_only': False}),
        ({'no_timestamp': False}, {'log_timestamp': True}),
        ({'no_timestamp': True}, {'log_timestamp': False}),
        ({'debug': True}, {'verbosity': 2}),
        ({'debug': False}, {'verbosity': 0}),
    ]
)
def test__schema_opts_to_api_opts(schema_opts, expect):
    """It converts items correctly.
    """
    result = _schema_opts_to_api_opts(schema_opts)
    assert SimpleNamespace(**expect) == result


def test__schema_opts_to_api_opts_fails():
    """It raises exception if value not in SCHEMA_TO_API dict
    """
    with pytest.raises(
        InvalidSchemaOptionError, match='^foo is not a valid.*$'
    ):
        _schema_opts_to_api_opts({'foo': 254})


from functools import partial

@pytest.mark.parametrize(
    'func_, expect',
    [
        (
            partial(list, 'foo'),
            [True, ['f', 'o', 'o']]
        ),
        (
            partial(int, 'foo'),
            [False, "invalid literal for int() with base 10: 'foo'"]
        )
    ]
)
@pytest.mark.asyncio
async def test__run_cmd_in_procpoolexecutor(func_, expect):
    """It returns pass or fail.
    """
    result = await services._run_cmd_in_procpoolexecutor(func_)
    assert result == expect


@pytest.mark.asyncio
async def test__run_cmd_in_procpoolexecutor_other_proc():
    """It returns runs a function in another proc.
    """
    result = await services._run_cmd_in_procpoolexecutor(
        getpid
    )
    assert result[1] != getpid()


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