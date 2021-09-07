# This file is a temporary solution for subscriptions with graphql_ws and
# Tornado, from the following pending PR to graphql-ws:
# https://github.com/graphql-python/graphql-ws/pull/25/files
# The file was copied from this revision:
# https://github.com/graphql-python/graphql-ws/blob/cf560b9a5d18d4a3908dc2cfe2199766cc988fef/graphql_ws/tornado.py

import getpass
from inspect import isawaitable, isclass
import socket

from asyncio import create_task, gather, wait, shield, sleep
from asyncio.queues import QueueEmpty
from tornado.websocket import WebSocketClosedError
from graphql.execution.executors.asyncio import AsyncioExecutor
from graphql.execution.middleware import MiddlewareManager
from graphql_ws.base import ConnectionClosedException, BaseConnectionContext, BaseSubscriptionServer
from graphql_ws.observable_aiter import setup_observable_extension
from graphql_ws.constants import (
    GQL_CONNECTION_ACK,
    GQL_CONNECTION_ERROR,
    GQL_COMPLETE
)

from typing import Union, Awaitable, Any, List, Tuple, Dict, Optional

from cylc.uiserver.handlers import parse_current_user

setup_observable_extension()

NO_MSG_DELAY = 1.0


class TornadoConnectionContext(BaseConnectionContext):
    def receive(self):
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


class TornadoSubscriptionServer(BaseSubscriptionServer):
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
        self.current_user = None
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
            if hasattr(mw, "auth"):
                self.current_user = parse_current_user(self.current_user)
                mw.current_user = self.current_user['name']
                mw.auth = self.auth
        return dict(
            params,
            return_promise=True,
            executor=AsyncioExecutor(loop=self.loop),
            backend=self.backend,
            middleware=MiddlewareManager(
                *middleware,
                wrap_in_promise=False
            ),
        )

    async def _handle(self, ws, request_context):
        connection_context = TornadoConnectionContext(ws, request_context)
        await self.on_open(connection_context)
        pending = set()
        while True:
            message = None
            try:
                if connection_context.closed:
                    raise ConnectionClosedException()
                message = connection_context.receive()
            except ConnectionClosedException:
                break
            except QueueEmpty:
                pass
            finally:
                if pending:
                    (_, pending) = await wait(pending, timeout=0, loop=self.loop)

            if message:
                task = create_task(
                    self.on_message(connection_context, message))
                pending.add(task)
            else:
                await sleep(NO_MSG_DELAY)

        self.on_close(connection_context)
        for task in pending:
            task.cancel()

    async def handle(self, ws, request_context=None):
        await shield(self._handle(ws, request_context), loop=self.loop)

    async def on_open(self, connection_context):
        pass

    def on_close(self, connection_context):
        remove_operations = list(connection_context.operations.keys())
        for op_id in remove_operations:
            self.unsubscribe(connection_context, op_id)

    async def on_connect(self, connection_context, payload):
        pass

    async def on_connection_init(self, connection_context, op_id, payload):
        try:
            await self.on_connect(connection_context, payload)
            await self.send_message(connection_context, op_type=GQL_CONNECTION_ACK)
        except Exception as e:
            await self.send_error(connection_context, op_id, e, GQL_CONNECTION_ERROR)
            await connection_context.close(1011)

    def execute(self, request_context, params):
        params['context_value'] = request_context
        return super().execute(request_context, params)

    async def send_execution_result(self, connection_context, op_id,
                                    execution_result):
        """
        Our schema contains a subscription ObjectType that contains other
        ObjectType's. These are resolved with functions that are awaitable,
        but the GraphQL is not able to understand that during a subscription
        operation.

        This workaround will iterate the schema object, and resolve/await
        each awaitable. Not elegant, but works.

        From: https://github.com/graphql-python/graphql-ws/issues/12#issuecomment-476989150
        """
        resolving_items: List[Awaitable[Any]] = []

        queue: List[Tuple[Any, Optional[Union[int, str]], Any]] = [
            (
                None,
                None,
                execution_result.data,
            ),
        ]

        while queue:
            container, key, item = queue.pop(0)

            if isinstance(item, list):
                self.__extend_list_item(queue, item)

            elif isinstance(item, dict):
                self.__extend_dict_item(queue, item)

            elif isawaitable(item):
                container = container if container is not None else queue
                key: Union[int, str] = key if key is not None else 0

                resolving_items.append(
                    self.__resolve_container_item(container, key, item))

        # FIXME: If we have multiple items in the queue, and one of them
        #        fails, then we won't send the execution results.
        #        We could use return_exceptions=True here, but it is not
        #        clear how we should proceed. Should we re-queue the
        #        failed item? Send the error? Ignore it? Log?
        await gather(*resolving_items)

        await super().send_execution_result(connection_context, op_id,
                                            execution_result)

        return None

    async def __resolve_container_item(
            self,
            container: Any,
            key: Union[int, str],
            item: Awaitable[Any],
    ) -> None:
        container[key] = await item

    def __extend_list_item(
            self,
            queue: List[Tuple[
                Union[List[Any], Dict[Union[int, str], Any]], Union[
                    int, str], Any]],
            item: List[Any],
    ) -> None:
        queue.extend(
            (
                item,
                index,
                value,
            )
            for index, value in enumerate(item)
        )

    def __extend_dict_item(
            self,
            queue: List[Tuple[
                Union[List[Any], Dict[Union[int, str], Any]], Union[
                    int, str], Any]],
            item: Dict[Union[int, str], Any],
    ) -> None:
        queue.extend(
            (
                item,
                key,
                value,
            )
            for key, value in item.items()
        )

    async def on_start(self, connection_context, op_id, params):
        execution_result = self.execute(
            connection_context.request_context, params)

        if isawaitable(execution_result):
            execution_result = await execution_result

        if not hasattr(execution_result, '__aiter__'):
            await self.send_execution_result(connection_context, op_id, execution_result)
        else:
            iterator = await execution_result.__aiter__()
            connection_context.register_operation(op_id, iterator)
            async for single_result in iterator:
                if not connection_context.has_operation(op_id):
                    break
                await self.send_execution_result(connection_context, op_id, single_result)
            await self.send_message(connection_context, op_id, GQL_COMPLETE)

    async def on_stop(self, connection_context, op_id):
        self.unsubscribe(connection_context, op_id)
