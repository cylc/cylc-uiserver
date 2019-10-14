# Copyright (C) 2019 NIWA & British Crown (Met Office) & Contributors.
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

import pytest

from cylc.uiserver.workflows_mgr import *
from cylc.flow.exceptions import ClientTimeout

from .conftest import TestAsyncClient


@pytest.mark.asyncio
async def test_workflow_request_client_timeout(async_client: TestAsyncClient):
    async_client.will_return(ClientTimeout)
    ctx, msg = await workflow_request(client=async_client, command='')
    assert not ctx
    assert 'timeout' in msg.lower()


@pytest.mark.asyncio
async def test_workflow_request_client_error(async_client: TestAsyncClient):
    async_client.will_return(ClientError)
    ctx, msg = await workflow_request(client=async_client, command='')
    assert not ctx
    assert not msg


@pytest.mark.asyncio
@pytest.mark.parametrize("returns,command,context,expected_ctx,expected_msg", [
    pytest.param(
        42, 'cmd', None, 'cmd', 42
    ),
    pytest.param(
        42, '', None, '', 42
    ),
    pytest.param(
        42, 'cmd', 'some-context', 'some-context', 42
    )
])
async def test_workflow_request(
        async_client: TestAsyncClient,
        returns,
        command,
        context,
        expected_ctx,
        expected_msg
):
    async_client.will_return(returns)
    ctx, msg = await workflow_request(
        client=async_client, command=command, context=context)
    assert expected_ctx == ctx
    assert expected_msg == msg
