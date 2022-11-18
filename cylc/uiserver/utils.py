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
