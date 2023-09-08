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

from functools import partial
from getpass import getuser
from unittest import mock
from unittest.mock import MagicMock
import pytest

from graphql_ws.constants import GRAPHQL_WS
from tornado.httputil import HTTPServerRequest
from tornado.testing import AsyncHTTPTestCase, get_async_test_timeout
from tornado.web import Application

from cylc.uiserver.handlers import SubscriptionHandler


class MyApplication(Application):
    ...


class SubscriptionHandlerTest(AsyncHTTPTestCase):
    """Test for SubscriptionHandler"""

    def get_app(self) -> Application:
        return MyApplication(
            handlers=[
                (
                    '/subscriptions',
                    SubscriptionHandler,
                    {'sub_server': None, 'resolvers': None}
                )
            ]
        )

    def _create_handler(self, logged_in=True):
        app = self.get_app()
        request = HTTPServerRequest(method='GET', uri='/subscriptions')
        request.connection = MagicMock()
        handler = SubscriptionHandler(application=app, request=request,
                                      sub_server=None, resolvers=None)

        if logged_in:
            handler.get
            _current_user = lambda: {'name': getuser()}
        else:
            handler.current_user = None
        return handler

    @pytest.mark.usefixtures("mock_authentication_yossarian")
    def test_websockets_subprotocol(self):
        handler = self._create_handler()
        assert handler.select_subprotocol(subprotocols=[]) == GRAPHQL_WS

    @pytest.mark.usefixtures("mock_authentication_yossarian")
    def test_websockets_check_origin_accepts_same_origin(self):
        """A request that includes the Host header must use the same
        value as the server host, or an error is raised.

        This prevents CORS attacks. In Cylc UI, it should work as we
        expect the Host header to be set by the browser when you navigate
        to the UI Server. Once your browser opens the WebSocket request
        it should match the Host of the UI Server.
        """
        handler = self._create_handler()
        host_header = 'ui.cylc'
        handler.request.headers['Host'] = host_header
        assert handler.check_origin(f'http://{host_header}')

    @pytest.mark.usefixtures("mock_authentication_yossarian")
    def test_websockets_check_origin_rejects_different_origin(self):
        """A request from a different Host MUST be blocked to prevent
        CORS attacks.

        This is the default after Tornado 4, and helps secure Cylc UI
        WebSocket endpoint. Change this behavior carefully.
        """
        handler = self._create_handler()
        host_header = 'ui.cylc'
        handler.request.headers['Host'] = host_header
        handler.request.headers['Origin'] = 'ui.notcylc'
        assert not handler.check_origin('http://ui.notcylc')

    @pytest.mark.usefixtures("mock_authentication_yossarian")
    def test_websockets_context(self):
        handler = self._create_handler()
        assert handler.request == handler.context['request']
        assert 'resolvers' in handler.context

    @pytest.mark.usefixtures("mock_authentication_yossarian")
    def test_websockets_queue(self):
        handler = self._create_handler()
        message = '{"message":"a message"}'
        assert handler.queue.empty()
        self.io_loop.run_sync(partial(handler.on_message, message),
                              get_async_test_timeout())
        assert not handler.queue.empty()
        assert message == self.io_loop.run_sync(handler.recv,
                                                get_async_test_timeout())
        assert handler.queue.empty()

    @pytest.mark.usefixtures("mock_authentication_yossarian")
    def test_assert_callback_handler_gets_called(self):
        handler = self._create_handler()
        handler.subscription_server = MagicMock()
        handler.subscription_server.handle = MagicMock()
        handler.subscription_server.handle.assert_not_called()
        self.io_loop.run_sync(handler.open,
                              get_async_test_timeout())
        handler.subscription_server.handle.assert_called_once()
