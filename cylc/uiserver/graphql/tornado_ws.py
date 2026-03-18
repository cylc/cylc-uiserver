# The MIT License (MIT)
#
# Copyright (c) 2016-Present Syrus Akbary
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
# ----------------------------------------------------------------------------
#
# This code was derived from coded in the graphql-ws project, and code that
# was offered to the graphql-ws project by members of the Cylc
# development team but not merged.
#
# * https://github.com/graphql-python/graphql-ws
# * https://github.com/graphql-python/graphql-ws/pull/25/files
#
# It has been evolved to suit and ported to graphql-core v3.

import asyncio
from asyncio.queues import QueueEmpty
from contextlib import suppress
from inspect import isawaitable
import json
from typing import (
    TYPE_CHECKING,
    Any,
    Iterable,
    Literal,
    Type,
)

from graphql import (
    ExecutionResult,
    GraphQLError,
    MiddlewareManager,
    parse,
    validate,
)
from graphql.pyutils import is_awaitable
from tornado.websocket import WebSocketClosedError

from cylc.flow.network.graphql import instantiate_middleware
from cylc.flow.network.graphql_subscribe import subscribe
from cylc.uiserver.authorise import AuthorizationMiddleware
from cylc.uiserver.schema import SUB_RESOLVER_MAPPING


if TYPE_CHECKING:
    from collections.abc import AsyncIterator

    from graphene import Schema
    from graphql import ExecutionContext
    from tornado.httputil import HTTPServerRequest

    from cylc.uiserver.authorise import Authorization
    from cylc.uiserver.handlers import SubscriptionHandler

    SendOperationType = Literal[
        "connection_ack", "ping", "pong", "next", "error", "complete"
    ]

NO_MSG_DELAY = 1.0

# See https://github.com/enisdenjo/graphql-ws/blob/master/PROTOCOL.md
WS_PROTOCOL = 'graphql-transport-ws'
GQL_CONNECTION_INIT: Literal["connection_init"] = (
    'connection_init'  # Client -> Server
)
GQL_CONNECTION_ACK: Literal["connection_ack"] = (
    'connection_ack'  # Server -> Client
)
GQL_PING: Literal["ping"] = 'ping'  # Bidirectional
GQL_PONG: Literal["pong"] = 'pong'  # Bidirectional
GQL_SUBSCRIBE: Literal["subscribe"] = 'subscribe'  # Client -> Server
GQL_NEXT: Literal["next"] = 'next'  # Server -> Client
GQL_ERROR: Literal["error"] = 'error'  # Server -> Client
GQL_COMPLETE: Literal["complete"] = 'complete'  # Bidrectional

REQ_HEADER_INFO = {
    'Host',
    'User-Agent',
    'Origin',
    'Connection',
    'Sec-Websocket-Version',
    'Sec-Websocket-Protocol',
}


class TornadoConnectionContext:
    def __init__(self, ws: 'SubscriptionHandler', request_context: dict):
        self.ws = ws
        self.operations: dict[str, 'AsyncIterator'] = {}
        self.request_context = request_context
        self.pending_tasks: set[asyncio.Task] = set()

    def has_operation(self, op_id: str):
        return op_id in self.operations

    def register_operation(self, op_id: str, async_iterator: 'AsyncIterator'):
        self.operations[op_id] = async_iterator

    def get_operation(self, op_id: str):
        return self.operations[op_id]

    def remove_operation(self, op_id: str):
        return self.operations.pop(op_id, None)

    @property
    def closed(self) -> bool:
        return self.ws.close_code is not None

    def remember_task(self, task: asyncio.Task) -> None:
        self.pending_tasks.add(task)
        task.add_done_callback(self.pending_tasks.discard)

    async def unsubscribe(self, op_id: str) -> None:
        async_iterator = self._unsubscribe(op_id)
        if (
            getattr(async_iterator, "future", None)
            and async_iterator.future.cancel()
        ):
            await async_iterator.future

    def _unsubscribe(self, op_id: str):
        async_iterator = self.remove_operation(op_id)
        if hasattr(async_iterator, "dispose"):
            async_iterator.dispose()
        return async_iterator

    async def unsubscribe_all(self):
        awaitables = [
            self.unsubscribe(op_id)
            for op_id in list(self.operations)
        ]
        for task in self.pending_tasks:
            task.cancel()
            awaitables.append(task)
        if awaitables:
            with suppress(asyncio.CancelledError):
                await asyncio.gather(*awaitables)


class TornadoSubscriptionServer:

    def __init__(
        self,
        schema: 'Schema',
        middleware: Iterable[Type],
        execution_context_class: 'Type[ExecutionContext]',
        auth: 'Authorization',
    ):
        self.schema = schema
        self.middleware = middleware
        self.execution_context_class = execution_context_class
        self.auth = auth

    async def execute(self, params):
        # Parse query to document
        try:
            document = parse(params['query'])
        except GraphQLError as error:
            return ExecutionResult(data=None, errors=[error])

        # Validate document against schema
        validation_errors = validate(self.schema.graphql_schema, document)
        if validation_errors:
            return ExecutionResult(data=None, errors=validation_errors)

        # execute subscription
        return await subscribe(
            self.schema.graphql_schema,
            document,
            **params['kwargs']
        )

    def process_message(
        self,
        connection_context: TornadoConnectionContext,
        parsed_message: dict,
    ) -> asyncio.Task[None]:
        """Process a message from the client"""
        task = asyncio.create_task(
            self._process_message(connection_context, parsed_message)
        )
        connection_context.remember_task(task)
        return task

    async def _process_message(
        self,
        connection_context: TornadoConnectionContext,
        parsed_message: dict,
    ) -> None:
        op_id = parsed_message.get("id")
        op_type = parsed_message.get("type")
        payload = parsed_message.get("payload")

        if op_type == GQL_CONNECTION_INIT:
            return await self.on_connection_init(connection_context)

        elif op_type == GQL_SUBSCRIBE:
            if not isinstance(payload, dict):
                raise AssertionError("The payload must be a dict")
            assert op_id, "The message must have an operation ID"
            params = self.get_graphql_params(connection_context, payload)
            return await self.on_subscribe(connection_context, op_id, params)

        elif op_type == GQL_COMPLETE:
            assert op_id, "The message must have an operation ID"
            await connection_context.unsubscribe(op_id)
            connection_context.request_context['sub_statuses'][op_id] = 'stop'
            return

        elif op_type == GQL_PING:
            return await self.send_message(connection_context, GQL_PONG)

        elif op_type == GQL_PONG:
            return

        else:
            connection_context.ws.close(
                4400, f"Invalid message type: {op_type}"
            )

    async def on_connection_init(
        self, connection_context: TornadoConnectionContext
    ) -> None:
        try:
            await self.send_message(
                connection_context, op_type=GQL_CONNECTION_ACK
            )
        except Exception as e:
            connection_context.ws.close(1011, str(e))

    def get_graphql_params(
        self, connection_context: TornadoConnectionContext, payload: dict
    ):
        # Create a new context object for each subscription,
        # which allows it to carry a unique subscription id.
        params = {
            "variable_values": payload.get("variables"),
            "operation_name": payload.get("operationName"),
            "context_value": dict(
                payload.get("context", connection_context.request_context)
            ),
            "subscribe_resolver_map": SUB_RESOLVER_MAPPING,
        }
        # If middleware get instantiated here (optional), they will
        # be local/private to each subscription.
        middleware = list(
            instantiate_middleware(self.middleware)
        )
        for mw in middleware:
            if isinstance(mw, AuthorizationMiddleware):
                mw.auth = self.auth
        return {
            'query': payload.get("query"),
            'kwargs': dict(
                params,
                middleware=MiddlewareManager(
                    *middleware,
                ),
                execution_context_class=self.execution_context_class,
            )
        }

    async def handle(self, ws: 'SubscriptionHandler', request_context: dict):
        await asyncio.shield(self._handle(ws, request_context))

    async def _handle(self, ws: 'SubscriptionHandler', request_context: dict):
        connection_context = TornadoConnectionContext(ws, request_context)
        while not connection_context.closed:
            try:
                message = connection_context.ws.recv_nowait()
            except QueueEmpty:
                await asyncio.sleep(NO_MSG_DELAY)
            else:
                self.on_message(connection_context, message)

        await connection_context.unsubscribe_all()

    async def on_subscribe(
        self,
        connection_context: TornadoConnectionContext,
        op_id: str,
        params: dict,
    ) -> None:
        """Run when the client starts a subscription.

        Execute the GraphQL subscription and send to the client each resulting
        delta in turn.

        This will not return until the subscription ends (e.g. workflow stops),
        at which point it will send a complete message to the client and
        clean up.
        """
        # Attempt to unsubscribe first in case we already have a subscription
        # with this id.
        await connection_context.unsubscribe(op_id)

        connection_context.request_context['sub_statuses'][op_id] = 'start'

        params['kwargs']['root_value'] = op_id
        execution_result = await self.execute(params)
        iterator = None
        try:
            if isawaitable(execution_result):
                execution_result = await execution_result
            if not hasattr(execution_result, '__aiter__'):
                await self.send_execution_result(
                    connection_context, op_id, execution_result)
            else:
                iterator = execution_result.__aiter__()
                connection_context.register_operation(op_id, iterator)
                async for single_result in iterator:
                    if not connection_context.has_operation(op_id):
                        break
                    await self.send_execution_result(
                        connection_context, op_id, single_result)
        except (GeneratorExit, asyncio.CancelledError):
            raise
        except Exception as e:
            with suppress(WebSocketClosedError):
                await self.send_message(
                    connection_context,
                    GQL_ERROR,
                    op_id,
                    payload=[{"message": str(e)}],
                )
        finally:
            if iterator:
                await iterator.aclose()

        # Complete the subscription from the server side:
        with suppress(WebSocketClosedError):
            await self.send_message(connection_context, GQL_COMPLETE, op_id)
        await connection_context.unsubscribe(op_id)
        connection_context.request_context['sub_statuses'].pop(op_id, None)

    async def send_message(
        self,
        connection_context: TornadoConnectionContext,
        op_type: 'SendOperationType',
        op_id: str | None = None,
        payload=None,
    ) -> None:
        message = self.build_message(op_type, op_id, payload)
        try:
            return await connection_context.ws.write_message(message)
        except WebSocketClosedError:
            resolvers = connection_context.request_context.get('resolvers')
            if resolvers is not None:
                request: HTTPServerRequest = (
                    connection_context.request_context['request']
                )
                headers: dict[str, Any] = {}
                headers.update(getattr(request, 'headers', {}))
                resolvers.log.warning(
                    '[GraphQL WS] Websocket closed on send'
                    f' (Op.Type: {op_type}, Op.ID: {op_id})'
                    f' to remote IP: {request.remote_ip}'
                )
                headers_string = ''
                for key, val in headers.items():
                    if key in REQ_HEADER_INFO:
                        headers_string += f'        {key}: {val} \n'
                resolvers.log.debug(
                    'Websocket closed on send, with request context: \n'
                    f'    Remote IP: {request.remote_ip} \n'
                    '    Request Header Info: \n'
                    f'{headers_string}'
                )
            # Raise exception, in order to exit the on_start subscription loop.
            raise

    @staticmethod
    def build_message(
        op_type: 'SendOperationType', op_id: str | None, payload
    ):
        assert op_type, "Message must have a type"
        message: dict[str, Any] = {"type": op_type}
        if op_id is not None:
            message["id"] = op_id
        if payload is not None:
            message["payload"] = payload
        return message

    async def send_execution_result(
        self,
        connection_context: TornadoConnectionContext,
        op_id: str,
        execution_result: ExecutionResult,
    ):
        # Resolve any pending promises
        if is_awaitable(execution_result.data):
            # TODO: never hit?
            await execution_result.data  # type: ignore[misc]
        if execution_result.data and 'logs' not in execution_result.data:
            request_context = connection_context.request_context
            await request_context['resolvers'].flow_delta_processed(
                request_context, op_id)

        result = execution_result.formatted
        return await self.send_message(
            connection_context, GQL_NEXT, op_id, result
        )

    def on_message(
        self, connection_context: TornadoConnectionContext, message
    ) -> None:
        try:
            parsed_message = json.loads(message)
            if not isinstance(parsed_message, dict):
                raise AssertionError("Message must be an object")
        except Exception as e:
            connection_context.ws.close(4400, str(e))
            return None

        self.process_message(connection_context, parsed_message)
