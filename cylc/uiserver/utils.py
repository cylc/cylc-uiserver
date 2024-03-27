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


from typing import TYPE_CHECKING

from jupyter_server.auth.identity import PasswordIdentityProvider

if TYPE_CHECKING:
    from cylc.uiserver.handlers import CylcAppHandler
    from jupyter_server.auth.identity import (
        IdentityProvider as JPSIdentityProvider,
    )


def is_bearer_token_authenticated(handler: 'CylcAppHandler') -> bool:
    """Returns True if this request is bearer token authenticated.

    Bearer tokens, e.g. tokens (?token=1234) and passwords, are short pieces of
    text that are used for authentication. These can be used in single-user
    mode (i.e. "cylc gui"). In these cases the bearer of the token is awarded
    full privileges.

    In multi-user mode, we have more advanced authentication based on an
    external service which allows us to implement fine-grained authorisation.
    """
    identity_provider: 'JPSIdentityProvider' = (
        handler.serverapp.identity_provider  # type: ignore[union-attr]
    )
    return identity_provider.__class__ == PasswordIdentityProvider
    # NOTE: not using isinstance to narrow this down to just the one class


def _repr(value):
    if isinstance(value, dict):
        return '<dict>'
    if isinstance(value, set):
        return '<set>'
    return repr(value)


def fmt_call(name, args, kwargs):
    """Format a Python function call.

    Examples:
        It formats calls at they would appear in Python code:
        >>> fmt_call('foo', (1,), {'x': True})
        'foo(1, x=True)'

        It handles different data types:
        >>> fmt_call('foo', ('str', 42, True, None), {})
        "foo('str', 42, True, None)"

        It puts in placeholders for dicts and sets (too long for log output):
        >>> fmt_call('foo', tuple(), {'a': {'x': 1}, 'b': {'y',}})
        'foo(a=<dict>, b=<set>)'

    """
    return f'{name}(' + ', '.join(
        [
            _repr(arg) for arg in args
        ] + [
            f'{key}={_repr(value)}'
            for key, value in kwargs.items()
        ]
    ) + ')'
