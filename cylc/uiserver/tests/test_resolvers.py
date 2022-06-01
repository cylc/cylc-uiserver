import pytest
from os import getpid
from types import SimpleNamespace

from cylc.uiserver.resolvers import (
    _schema_opts_to_api_opts,
    InvalidSchemaOptionError,
    _clean,
    Services
)


services = Services()


@pytest.mark.parametrize(
    'schema_opts, expect',
    [
        ([{'rm': ''}, 'clean'], {'rm_dirs': ['']}),
        ([{'rm': 'work:share'}, 'clean'], {'rm_dirs': ['work', 'share']}),
        ([{'local_only': True}, 'clean'], {'local_only': True}),
        ([{'remote_only': False}, 'clean'], {'remote_only': False}),
        ([{'no_timestamp': False}, 'clean'], {'log_timestamp': True}),
        ([{'no_timestamp': True}, 'clean'], {'log_timestamp': False}),
        ([{'debug': True}, 'clean'], {'verbosity': 2}),
        ([{'debug': False}, 'clean'], {'verbosity': 0}),
    ]
)
def test__schema_opts_to_api_opts(schema_opts, expect):
    """It converts items correctly.
    """
    result = _schema_opts_to_api_opts(*schema_opts)
    assert SimpleNamespace(**expect) == result


def test__schema_opts_to_api_opts_fails():
    """It raises exception if value not in SCHEMA_TO_API dict
    """
    with pytest.raises(
        InvalidSchemaOptionError, match='^foo is not a valid.*$'
    ):
        _schema_opts_to_api_opts({'foo': 254}, 'clean')


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
