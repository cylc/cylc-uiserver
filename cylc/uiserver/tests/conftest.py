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

import inspect

import pytest
import zmq

from cylc.flow.network import ZMQSocketBase


class AsyncClientFixture(ZMQSocketBase):
    pattern = zmq.REQ
    host = ''
    port = 0

    def __init__(self):
        self.returns = None

    def will_return(self, returns):
        self.returns = returns

    async def async_request(self, command, args=None, timeout=None):
        if inspect.isclass(self.returns) and \
                issubclass(self.returns, Exception):
            raise self.returns
        return self.returns


@pytest.fixture
def async_client():
    return AsyncClientFixture()
