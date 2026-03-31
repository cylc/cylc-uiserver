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
import json
from unittest import mock
from unittest.mock import MagicMock
import pytest

from graphql import ExecutionResult, GraphQLError
from graphql.execution.middleware import MiddlewareManager
from tornado.httputil import HTTPServerRequest
from tornado.testing import AsyncHTTPTestCase, get_async_test_timeout, gen_test
from tornado.web import Application
from tornado.web import HTTPError

from cylc.flow.network.graphql import (
    CylcExecutionContext, IgnoreFieldMiddleware
)
from cylc.uiserver.authorise import AuthorizationMiddleware
from cylc.uiserver.graphql.tornado import TornadoGraphQLHandler, ExecutionError
from cylc.uiserver.graphql.tornado_ws import GRAPHQL_WS
from cylc.uiserver.handlers import (
    SubscriptionHandler,
    UIServerGraphQLHandler,
)
from cylc.uiserver.schema import schema


class MyApplication(Application):
    ...

class GraphQLHandlersTest(AsyncHTTPTestCase):
    """Test for TornadoGraphQLHandler/UIServerGraphQLHandler"""

    def get_app(self, handler_class=UIServerGraphQLHandler) -> Application:
        return MyApplication(
            handlers=[
                (
                    'graphql',
                    handler_class,
                    {
                        'schema': schema,
                        'middleware': [
                            AuthorizationMiddleware,
                            IgnoreFieldMiddleware
                        ],
                        'execution_context_class': CylcExecutionContext,
                    }
                ),
            ]
        )

    def _create_handler(
        self,
        handler_class=UIServerGraphQLHandler,
        r_kwargs={},
        h_kwargs={},
        logged_in=True,
    ):
        app = self.get_app(handler_class)
        r_params = {
            'uri': '/graphql',
            'method': 'GET',
            **r_kwargs,
        }
        request = HTTPServerRequest(**r_params)
        request.connection = MagicMock()
        h_params = {
            'middleware': [
                AuthorizationMiddleware,
                IgnoreFieldMiddleware
            ],
            'execution_context_class': CylcExecutionContext,
            **h_kwargs,
        }
        handler = handler_class(
            application=app,
            request=request,
            schema=schema,
            **h_params,
        )

        if logged_in:
            handler.get
            _current_user = lambda: {'name': getuser()}
        else:
            handler.current_user = None
        return handler

    def test_setup(self):
        """Test setup, attributes, and properties."""
        mid_manager = MiddlewareManager()
        handler = self._create_handler(
            handler_class=TornadoGraphQLHandler,
            h_kwargs={'middleware': mid_manager}
        )
        assert handler.middleware == mid_manager

        handler = self._create_handler(
            handler_class=TornadoGraphQLHandler,
            h_kwargs={'middleware': None},
        )
        assert not handler.middleware
        assert handler.get_context().method == "GET"

    def test_parse_body(self):
        """Test parse_body for query doc."""
        handler = self._create_handler(
            r_kwargs={
                'headers': {'Content-Type': "application/json"},
                'method': "POST",
            }
        )
        assert not handler.get_parsed_body()

        class FakeRequest:
            headers = {'Content-Type': "Application/json"}
            errors = None

        # test request without body.
        orig_request = handler.request
        handler.request = FakeRequest()
        with pytest.raises(ExecutionError) as exc:
            handler.parse_body()
        assert 'FakeRequest' in str(exc)

        ex_error = ExecutionError(123, None)
        assert ex_error.status_code == 123
        assert ex_error.message == ''

        # test invalid JSON string
        handler.request = orig_request
        handler.request.body = '%&^ds:ea43#'
        with pytest.raises(HTTPError) as exc:
            handler.parse_body()
        assert 'invalid JSON' in str(exc.value)

        # test invalid query
        handler.request.body = json.dumps([{'this': "that"}])
        with pytest.raises(HTTPError) as exc:
            handler.parse_body()
        assert 'not a valid JSON query.' in str(exc.value)

    @gen_test
    @pytest.mark.usefixtures("mock_authentication_yossarian")
    async def test_get_response(self):
        """Test get_response."""
        r_kwargs = {
            'headers': {'Content-Type': "application/json"},
            'method': "POST",
            'body': json.dumps({'query': "curry { massaman }"})
        }
        h_kwargs = {
            'execution_context_class': None,
            'parsed_body': 'cake',
        }
        handler = self._create_handler(r_kwargs=r_kwargs, h_kwargs=h_kwargs)
        assert handler.parsed_body == 'cake'

        # Test bad query
        data = handler.parse_body()
        result, status_code = await handler.get_response(data)
        assert status_code == 400
        assert 'curry' in result

        # Test good query
        doc = {
            'query': '''
                query stoke ($wFlows: [ID]){
                  workflows (ids: $wFlows) { id status }
                }
            ''',
            'variables': {'wFlows': ["*/run1"]},
            'operationName': 'stoke',
        }

        handler.request.body = json.dumps(doc)
        data = handler.parse_body()
        handler.graphql_params = {}
        result, status_code = await handler.get_response(data)
        assert status_code == 200
        # caught by auth
        assert 'Forbidden' in str(result)
        assert handler.graphql_params[2] == 'stoke'
        # test the graphql params bypass
        result, status_code = await handler.get_response(data)
        assert status_code == 200
        assert 'Forbidden' in str(result)

        # test bad schema
        orig_type = handler.schema.graphql_schema.query_type
        handler.schema.graphql_schema.query_type = None
        result, status_code = await handler.get_response(data)
        assert 'not configured to execute query' in result
        assert status_code == 400
        handler.schema.graphql_schema.query_type = orig_type
        handler.schema.graphql_schema._validation_errors = ['nasty one']
        result, status_code = await handler.get_response(data)
        assert 'nasty one' in result
        assert status_code == 400
        handler.schema.graphql_schema._validation_errors = []

        # by-pass auth middleware
        h_kwargs['middleware'] = []
        doc['operationName'] = 'null'
        handler = self._create_handler(r_kwargs=r_kwargs, h_kwargs=h_kwargs)
        handler.request.body = json.dumps(doc)
        data = handler.parse_body()
        handler.graphql_params = {}
        result, status_code = await handler.get_response(data)
        assert status_code == 200
        # because no resolvers set:
        assert "object has no attribute 'get_workflows'" in str(result)
        # operationName should be None
        assert handler.graphql_params[2] is None

        # test invalid variable
        doc['variables'] = 'Nope'
        handler.request.body = json.dumps(doc)
        data = handler.parse_body()
        handler.graphql_params = {}
        with pytest.raises(HTTPError) as exc:
            await handler.get_response(data)
        assert 'Variables are invalid JSON' in str(exc.value)

        doc['variables'] = {'wFlows': ["*/run1"]},
        doc['operationName'] = 'stoke'
        handler.request.body = json.dumps(doc)
        data = handler.parse_body()
        handler.graphql_params = {}

        # test execution error
        async def exec_error(schema, doc, **kwargs):
            raise ExecutionError(400, ['problems'])
        orig_exec = handler.execute
        handler.execute = exec_error
        result, status_code = await handler.get_response(data)
        assert status_code == 400
        handler.execute = orig_exec

        # replicate the None result
        async def exe_gql_req(data, query, variables, operation_name):
            return None
        handler.execute_graphql_request = exe_gql_req
        result, status_code = await handler.get_response(data)
        assert status_code == 200
        assert result is None

        # test an execution result with get method (i.e. other api link)
        async def exe_gql_req2(data, query, variables, operation_name):
            class FakeResult:
                def get(self):
                    return ExecutionResult(data='other-api-response')
            return FakeResult()
        handler.execute_graphql_request = exe_gql_req2
        result, status_code = await handler.get_response(data)
        assert status_code == 200
        assert 'other-api-response' in result

        # test an execution result with errors
        async def exe_gql_req3(data, query, variables, operation_name):
            return ExecutionResult(
                errors = [
                    GraphQLError('GQL error'),
                    ExecutionError(400, ['Some Exc error']),
                    Exception('random other error')
                ]
            )
        handler.execute_graphql_request = exe_gql_req3
        result, status_code = await handler.get_response(data)
        assert status_code == 400
        assert 'GQL error' in result
        assert 'Some Exc error' in result
        assert 'random other error' in result


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


@pytest.mark.integration
async def test_userprofile(
    jp_fetch, cylc_uis, jp_serverapp,
):
    """Test the userprofile endpoint."""
    # patch the default_url back to how it is set in cylc.uiserver.app
    cylc_uis.default_url = '/cylc'

    response = await jp_fetch('cylc', 'userprofile')
    user_profile = json.loads(response.body.decode())
    assert user_profile['username'] == getuser()
    assert user_profile['owner'] == getuser()
    assert 'read' in user_profile['permissions']
    assert 'cylc' in user_profile['extensions']
