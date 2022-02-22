import pytest

from types import SimpleNamespace

from cylc.uiserver.resolvers import (
    _schema_opts_to_api_opts,
    InvalidSchemaOptionError,
)

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
