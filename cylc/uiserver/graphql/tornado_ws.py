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
from weakref import WeakSet

from tornado.websocket import WebSocketClosedError
from graphql import (
    parse,
    validate,
    ExecutionResult,
    GraphQLError,
    MiddlewareManager,
)
from graphql.pyutils import is_awaitable

from cylc.flow.network.graphql import instantiate_middleware
from cylc.flow.network.graphql_subscribe import subscribe

from cylc.uiserver.authorise import AuthorizationMiddleware
from cylc.uiserver.schema import SUB_RESOLVER_MAPPING


NO_MSG_DELAY = 1.0

GRAPHQL_WS = "graphql-ws"
WS_PROTOCOL = GRAPHQL_WS
GQL_CONNECTION_INIT = "connection_init"  # Client -> Server
GQL_CONNECTION_ACK = "connection_ack"  # Server -> Client
GQL_CONNECTION_ERROR = "connection_error"  # Server -> Client
GQL_CONNECTION_TERMINATE = "connection_terminate"  # Client -> Server
GQL_CONNECTION_KEEP_ALIVE = "ka"  # Server -> Client
GQL_START = "start"  # Client -> Server
GQL_DATA = "data"  # Server -> Client
GQL_ERROR = "error"  # Server -> Client
GQL_COMPLETE = "complete"  # Server -> Client
GQL_STOP = "stop"  # Client -> Server


class ConnectionClosedException(Exception):
    pass


class TornadoConnectionContext:

    def __init__(self, ws, request_context=None):
        self.ws = ws
        self.operations = {}
        self.request_context = request_context
        self.pending_tasks = WeakSet()

    def has_operation(self, op_id):
        return op_id in self.operations

    def register_operation(self, op_id, async_iterator):
        self.operations[op_id] = async_iterator

    def get_operation(self, op_id):
        return self.operations[op_id]

    def remove_operation(self, op_id):
        try:
            return self.operations.pop(op_id)
        except KeyError:
            return

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

    def remember_task(self, task):
        self.pending_tasks.add(task)
        # Clear completed tasks
        self.pending_tasks -= WeakSet(
            task for task in self.pending_tasks if task.done()
        )

    async def unsubscribe(self, op_id):
        async_iterator = self._unsubscribe(op_id)
        if (
            getattr(async_iterator, "future", None)
            and async_iterator.future.cancel()
        ):
            await async_iterator.future

    def _unsubscribe(self, op_id):
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
        schema,
        keep_alive=True,
        loop=None,
        middleware=None,
        execution_context_class=None,
        auth=None
    ):
        self.schema = schema
        self.loop = loop
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

    def process_message(self, connection_context, parsed_message):
        task = asyncio.ensure_future(
            self._process_message(connection_context, parsed_message),
            loop=self.loop
        )
        connection_context.remember_task(task)
        return task

    async def _process_message(self, connection_context, parsed_message):
        op_id = parsed_message.get("id")
        op_type = parsed_message.get("type")
        payload = parsed_message.get("payload")

        if op_type == GQL_CONNECTION_INIT:
            return await self.on_connection_init(
                connection_context, op_id, payload
            )

        elif op_type == GQL_CONNECTION_TERMINATE:
            return self.on_connection_terminate(connection_context, op_id)

        elif op_type == GQL_START:
            if not isinstance(payload, dict):
                raise AssertionError("The payload must be a dict")
            params = self.get_graphql_params(connection_context, payload)
            return await self.on_start(connection_context, op_id, params)

        elif op_type == GQL_STOP:
            return await self.on_stop(connection_context, op_id)

        else:
            return await self.send_error(
                connection_context,
                op_id,
                Exception("Invalid message type: {}.".format(op_type)),
            )

    async def on_connection_init(self, connection_context, op_id, payload):
        try:
            await self.on_connect(connection_context, payload)
            await self.send_message(
                connection_context, op_type=GQL_CONNECTION_ACK)
        except Exception as e:
            await self.send_error(
                connection_context, op_id, e, GQL_CONNECTION_ERROR)
            await connection_context.close(1011)

    async def on_connect(self, connection_context, payload):
        pass

    def on_connection_terminate(self, connection_context, op_id):
        return connection_context.close(1011)

    def get_graphql_params(self, connection_context, payload):
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
        if self.middleware is not None:
            middleware = list(
                instantiate_middleware(self.middleware)
            )
        else:
            middleware = self.middleware
        for mw in self.middleware:
            if mw == AuthorizationMiddleware:
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

    async def on_open(self, connection_context):
        pass

    async def on_stop(self, connection_context, op_id):
        return await connection_context.unsubscribe(op_id)

    async def on_close(self, connection_context):
        return await connection_context.unsubscribe_all()

    async def handle(self, ws, request_context=None):
        await asyncio.shield(self._handle(ws, request_context))

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
                await self.on_message(connection_context, message)
            else:
                await asyncio.sleep(NO_MSG_DELAY)

        await self.on_close(connection_context)

    async def on_start(self, connection_context, op_id, params):
        # Attempt to unsubscribe first in case we already have a subscription
        # with this id.
        await connection_context.unsubscribe(op_id)

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
            await self.send_error(connection_context, op_id, e)
        finally:
            if iterator:
                await iterator.aclose()
        await self.send_message(connection_context, op_id, GQL_COMPLETE)
        await connection_context.unsubscribe(op_id)
        await self.on_operation_complete(connection_context, op_id)

    async def send_message(
        self, connection_context, op_id=None, op_type=None, payload=None
    ):
        message = self.build_message(op_id, op_type, payload)
        return await connection_context.send(message)

    def build_message(self, _id, op_type, payload):
        message = {}
        if _id is not None:
            message["id"] = _id
        if op_type is not None:
            message["type"] = op_type
        if payload is not None:
            message["payload"] = payload
        if not message:
            raise AssertionError("You need to send at least one thing")
        return message

    async def send_execution_result(
            self, connection_context, op_id, execution_result):
        # Resolve any pending promises
        if is_awaitable(execution_result.data):
            await execution_result.data
        if execution_result.data and 'logs' not in execution_result.data:
            request_context = connection_context.request_context
            await request_context['resolvers'].flow_delta_processed(
                request_context, op_id)

        result = execution_result.formatted
        return await self.send_message(
            connection_context, op_id, GQL_DATA, result
        )

    async def on_operation_complete(self, connection_context, op_id):
        # remove the subscription from the sub_statuses dict
        with suppress(KeyError):
            connection_context.request_context['sub_statuses'].pop(op_id)

    async def send_error(
        self, connection_context, op_id, error, error_type=None
    ):
        if error_type is None:
            error_type = GQL_ERROR

        if error_type not in {GQL_CONNECTION_ERROR, GQL_ERROR}:
            raise AssertionError(
                "error_type should be one of the allowed error messages"
                " GQL_CONNECTION_ERROR or GQL_ERROR"
            )

        error_payload = {"message": str(error)}

        return await self.send_message(
            connection_context, op_id, error_type, error_payload)

    async def on_message(self, connection_context, message):
        try:
            if not isinstance(message, dict):
                parsed_message = json.loads(message)
                if not isinstance(parsed_message, dict):
                    raise AssertionError("Payload must be an object.")
            else:
                parsed_message = message
        except Exception as e:
            return await self.send_error(connection_context, None, e)

        return self.process_message(connection_context, parsed_message)
