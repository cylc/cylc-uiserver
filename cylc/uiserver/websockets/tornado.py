# This file is a temporary solution for subscriptions with graphql_ws and
# Tornado, from the following pending PR to graphql-ws:
# https://github.com/graphql-python/graphql-ws/pull/25/files
# The file was copied from this revision:
# https://github.com/graphql-python/graphql-ws/blob/cf560b9a5d18d4a3908dc2cfe2199766cc988fef/graphql_ws/tornado.py

from contextlib import suppress
import getpass
from inspect import isawaitable, isclass
import socket

from asyncio import create_task, gather, wait, shield, sleep
from asyncio.queues import QueueEmpty
from tornado.websocket import WebSocketClosedError
from graphql.execution.middleware import MiddlewareManager
from graphql_ws.base import ConnectionClosedException, BaseSubscriptionServer
from graphql_ws.base_async import (
    BaseAsyncConnectionContext,
    BaseAsyncSubscriptionServer
)
from graphql_ws.observable_aiter import setup_observable_extension
from graphql_ws.constants import (
    GQL_CONNECTION_ACK,
    GQL_CONNECTION_ERROR,
    GQL_COMPLETE
)

from typing import Union, Awaitable, Any, List, Tuple, Dict, Optional

from cylc.uiserver.authorise import AuthorizationMiddleware
from cylc.uiserver.websockets.resolve import resolve


setup_observable_extension()

NO_MSG_DELAY = 1.0


class TornadoConnectionContext(BaseAsyncConnectionContext):
    async def receive(self):
        try:
            return self.ws.recv_nowait()
        except WebSocketClosedError:
            raise ConnectionClosedException()

    async def send(self, data):
        if self.closed:
            return
        await self.ws.write_message(data)

    @property
    def closed(self):
        return self.ws.close_code is not None

    async def close(self, code):
        await self.ws.close(code)


class TornadoSubscriptionServer(BaseAsyncSubscriptionServer):
    def __init__(
        self, schema,
        keep_alive=True,
        loop=None,
        backend=None,
        middleware=None,
        auth=None
    ):
        self.loop = loop
        self.backend = backend or None
        self.middleware = middleware
        self.auth = auth
        super().__init__(schema, keep_alive)

    @staticmethod
    def instantiate_middleware(middlewares):
        for middleware in middlewares:
            if isclass(middleware):
                yield middleware()
                continue
            yield middleware

    def get_graphql_params(self, *args, **kwargs):
        params = super(TornadoSubscriptionServer,
                       self).get_graphql_params(*args, **kwargs)
        # If middleware get instantiated here (optional), they will
        # be local/private to each subscription.
        if self.middleware is not None:
            middleware = list(
                self.instantiate_middleware(self.middleware)
            )
        else:
            middleware = self.middleware
        for mw in self.middleware:
            if mw == AuthorizationMiddleware:
                mw.auth = self.auth
        return dict(
            params,
            return_promise=True,
            backend=self.backend,
            middleware=MiddlewareManager(
                *middleware,
                wrap_in_promise=False
            ),
        )

    async def _handle(self, ws, request_context=None):
        connection_context = TornadoConnectionContext(ws, request_context)
        await self.on_open(connection_context)
        while True:
            message = None
            try:
                if connection_context.closed:
                    raise ConnectionClosedException()
                message = await connection_context.receive()
            except QueueEmpty:
                pass
            except ConnectionClosedException:
                break
            if message:
                self.on_message(connection_context, message)
            else:
                await sleep(NO_MSG_DELAY)

        await self.on_close(connection_context)

    async def handle(self, ws, request_context=None):
        await shield(self._handle(ws, request_context))

    async def on_start(self, connection_context, op_id, params):
        # Attempt to unsubscribe first in case we already have a subscription
        # with this id.
        await connection_context.unsubscribe(op_id)

        params['root_value'] = op_id
        execution_result = self.execute(params)
        try:
            if isawaitable(execution_result):
                execution_result = await execution_result
            if not hasattr(execution_result, '__aiter__'):
                await self.send_execution_result(
                    connection_context, op_id, execution_result)
            else:
                iterator = await execution_result.__aiter__()
                connection_context.register_operation(op_id, iterator)
                async for single_result in iterator:
                    if not connection_context.has_operation(op_id):
                        break
                    await self.send_execution_result(
                        connection_context, op_id, single_result)
        except Exception as e:
            await self.send_error(connection_context, op_id, e)
        await self.send_message(connection_context, op_id, GQL_COMPLETE)
        await connection_context.unsubscribe(op_id)
        await self.on_operation_complete(connection_context, op_id)

    async def on_operation_complete(self, connection_context, op_id):
        # remove the subscription from the sub_statuses dict
        with suppress(KeyError):
            connection_context.request_context['sub_statuses'].pop(op_id)


    async def send_execution_result(self, connection_context, op_id, execution_result):
        # Resolve any pending promises
        if execution_result.data and 'logs' not in execution_result.data:
            await resolve(execution_result.data)
            request_context = connection_context.request_context
            await request_context['resolvers'].flow_delta_processed(request_context, op_id)
        else:
            await resolve(execution_result.data)

        # NOTE: skip TornadoSubscriptionServer.send_execution_result because it
        # calls "resolve" then invokes BaseSubscriptionServer.send_execution_result
        await BaseSubscriptionServer.send_execution_result(
            self,
            connection_context,
            op_id,
            execution_result,
        )
