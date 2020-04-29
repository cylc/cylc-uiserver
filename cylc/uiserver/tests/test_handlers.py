# -*- coding: utf-8 -*-
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

import os
import shutil
import tempfile
from functools import partial
from unittest.mock import patch, MagicMock

from graphql_ws.constants import GRAPHQL_WS
from tornado.httpclient import HTTPResponse
from tornado.httputil import HTTPServerRequest
from tornado.testing import AsyncHTTPTestCase, get_async_test_timeout
from tornado.web import Application

from cylc.uiserver.handlers import *
from cylc.uiserver.main import *


class MainHandlerTest(AsyncHTTPTestCase):
    """Test for the Main handler"""

    def get_app(self) -> Application:
        self.tempdir = tempfile.mkdtemp(suffix='mainhandlertest')
        return MyApplication(
            handlers=[
                ('/', MainHandler, {"path": self.tempdir})
            ]
        )

    def test_jupyterhub_version_returned(self):
        with patch.object(MainHandler, 'get_current_user') as mocked:
            mocked.return_value = {
                'name': 'yossarian',
                'server': 'catch:22'
            }
            with open(os.path.join(self.tempdir, "index.html"), "w+") as nf:
                nf.write("TESTING!")
                nf.flush()
                response = self.fetch("/")  # type: HTTPResponse
                assert response.body == b"TESTING!"
                assert "X-JupyterHub-Version" in response.headers

    def tearDown(self) -> None:
        if self.tempdir:
            shutil.rmtree(self.tempdir, ignore_errors=True)


class UserProfileHandlerTest(AsyncHTTPTestCase):
    """Test for UserProfile handler"""

    def get_app(self) -> Application:
        return MyApplication(
            handlers=[
                ('/userprofile', UserProfileHandler)
            ]
        )

    def test_user_profile_handler_cors_headers(self):
        with patch.object(UserProfileHandler, 'get_current_user') as mocked:
            mocked.return_value = {
                'name': 'yossarian',
                'server': 'catch:22'
            }
            response = self.fetch("/userprofile")  # type: HTTPResponse
            assert "Access-Control-Allow-Origin" in response.headers
            assert "Access-Control-Allow-Headers" in response.headers
            assert "Access-Control-Allow-Methods" in response.headers
            assert "Content-Type" in response.headers
            assert b'yossarian' in response.body


class SubscriptionHandlerTest(AsyncHTTPTestCase):
    """Test for SubscriptionHandler"""

    def get_app(self) -> Application:
        return MyApplication(
            handlers=[
                ('/subscriptions', SubscriptionHandler,
                 dict(sub_server=None, resolvers=None))
            ]
        )

    def test_websockets_reject_get_requests(self):
        response = self.fetch('/subscriptions')
        assert 400 == response.code
        assert b"WebSocket" in response.body

    def _create_handler(self):
        app = self.get_app()
        request = HTTPServerRequest(method='GET', uri='/subscriptions')
        request.connection = MagicMock()
        return SubscriptionHandler(application=app, request=request,
                                   sub_server=None, resolvers=None)

    def test_websockets_subprotocol(self):
        handler = self._create_handler()
        assert handler.select_subprotocol(subprotocols=[]) == GRAPHQL_WS

    def test_websockets_check_origin(self):
        handler = self._create_handler()
        assert handler.check_origin(origin='')

    def test_websockets_context(self):
        handler = self._create_handler()
        assert handler.request == handler.context['request']
        assert 'resolvers' in handler.context

    def test_websockets_queue(self):
        handler = self._create_handler()
        message = 'a message'
        assert handler.queue.empty()
        self.io_loop.run_sync(partial(handler.on_message, message),
                              get_async_test_timeout())
        assert not handler.queue.empty()
        assert message == self.io_loop.run_sync(handler.recv,
                                                get_async_test_timeout())
        assert handler.queue.empty()

    def test_assert_callback_handler_gets_called(self):
        handler = self._create_handler()
        handler.subscription_server = MagicMock()
        handler.subscription_server.handle = MagicMock()
        handler.subscription_server.handle.assert_not_called()
        self.io_loop.run_sync(handler.open,
                              get_async_test_timeout())
        handler.subscription_server.handle.assert_called_once()
