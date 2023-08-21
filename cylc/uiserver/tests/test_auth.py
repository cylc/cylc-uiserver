#!/usr/bin/env python3
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
"""Test authorisation and authentication HTTP response codes."""

from functools import partial

import pytest
from tornado.httpclient import HTTPClientError


@pytest.mark.integration
@pytest.mark.usefixtures("mock_authentication_yossarian")
async def test_cylc_handler(patch_conf_files, jp_fetch):
    """The Cylc endpoints have been added and work."""
    resp = await jp_fetch(
        'cylc', 'userprofile', method='GET'
    )
    assert resp.code == 200


@pytest.mark.integration
@pytest.mark.usefixtures("mock_authentication_yossarian")
@pytest.mark.parametrize(
    'endpoint,code,message,body',
    [
        pytest.param(
            ('cylc', 'graphql'),
            400,
            None,
            b'Must provide query string',
            id='cylc/graphql',
        ),
        pytest.param(
            ('cylc', 'subscriptions'),
            400,
            None,
            b'WebSocket',
            id='cylc/subscriptions',
        ),
        pytest.param(
            ('cylc', 'userprofile'),
            200,
            None,
            b'"name":',
            id='cylc/userprofile',
        )
    ]
)
async def test_authorised_and_authenticated(
    patch_conf_files,
    jp_fetch,
    endpoint,
    code,
    message,
    body
):
    await _test(jp_fetch, endpoint, code, message, body)


@pytest.mark.integration
@pytest.mark.usefixtures("mock_authentication_yossarian")
@pytest.mark.parametrize(
    'endpoint,code,message,body',
    [
        pytest.param(
            # should pass through authentication but fail as there is no query
            ('cylc', 'graphql'),
            400,
            'Bad Request',
            None,
            id='cylc/graphql',
        ),
        pytest.param(
            # should pass through authentication but fail as there is no query
            # (authorisation is performed in the grahpql layer)
            ('cylc', 'subscriptions'),
            400,
            'Bad Request',
            None,
            id='cylc/subscriptions',
        ),
    ]
)
async def test_unauthorised(
    patch_conf_files,
    jp_fetch,
    endpoint,
    code,
    message,
    body
):
    await _test(jp_fetch, endpoint, code, message, body)


@pytest.fixture
def authorisation_middleware_instances(monkeypatch):
    """Captures instances of the AuthorizationMiddleware class.

    Returns a list which is updated with instances of AuthorizationMiddleware
    created within the lifetime of the test function.
    """
    instances = []

    def _init(self):
        nonlocal instances
        instances.append(self)

    monkeypatch.setattr(
        'cylc.uiserver.authorise.AuthorizationMiddleware.__init__',
        _init
    )

    return instances


async def _test(jp_fetch, endpoint, code, message, body):
    """Test 400 HTTP response (upgrade to websocket)."""
    fetch = partial(jp_fetch, *endpoint)
    if code != 200:
        # failure cases, test the exception
        with pytest.raises(HTTPClientError) as exc_ctx:
            await fetch()
        exc = exc_ctx.value
        assert exc.code == code
        if message:
            assert exc.message == message
        if body:
            assert body in exc.response.body
    else:
        # success cases, test the response
        response = await fetch()
        assert code == response.code
        if message:
            assert response.reason == message
        if body:
            assert body in response.body
