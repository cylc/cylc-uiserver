# MIT License
#
# Copyright (c) 2017, Syrus Akbary
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""
This file contains an implementation of "resolve" derived from the one
found in the graphql-ws library with the above license.

This is temporary code until the change makes its way upstream.
"""

# NOTE: transient dependency from graphql-ws purposefully not
# reflected in cylc-uiserver dependencies
from promise import Promise

from graphql_ws.base_async import is_awaitable


async def resolve(
    data,
    _container=None,
    _key=None,
):
    """
    Wait on any awaitable children of a data element and resolve
    any Promises.
    """
    stack = [(data, _container, _key)]

    while stack:
        _data, _container, _key = stack.pop()

        if is_awaitable(_data):
            _data = await _data
            if isinstance(_data, Promise):
                _data = _data.value
            if _container is not None:
                _container[_key] = _data
        if isinstance(_data, dict):
            items = _data.items()
        elif isinstance(_data, list):
            items = enumerate(_data)
        else:
            items = None
        if items is not None:
            stack.extend([
                (child, _data, key)
                for key, child in items
            ])
