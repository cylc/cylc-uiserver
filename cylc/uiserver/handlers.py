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

import json
import os
from asyncio import Queue, iscoroutinefunction
import logging
import getpass

from graphene_tornado.tornado_graphql_handler import TornadoGraphQLHandler
from graphql import get_default_backend
from graphql_ws.constants import GRAPHQL_WS
from jupyterhub import __version__ as jupyterhub_version
from jupyterhub.services.auth import HubOAuthenticated
from tornado import web, websocket
from tornado.ioloop import IOLoop

from .websockets import authenticated as websockets_authenticated
from .authorise import AuthorizationMiddleware, Authorization

logger = logging.getLogger(__name__)

ME = getpass.getuser()


def read_authorised():
    def authorise_inner(fun):
        if iscoroutinefunction(fun):
            async def decorated_func(self, *args, **kwargs):
                allowed, username = can_read(handler=self)
                if not allowed:
                    logger.warn(f'Authorization failed for {username}')
                    raise web.HTTPError(
                        403, reason='authorization insufficient')
                return await fun(self, *args, **kwargs)
            return decorated_func
        else:
            def decorated_func(self, *args, **kwargs):
                allowed, username = can_read(handler=self)
                if not allowed:
                    logger.warn(f'Authorization failed for {username}')
                    raise web.HTTPError(
                        403, reason='authorization insufficient')
                return fun(self, *args, **kwargs)
            return decorated_func
    return authorise_inner


def can_read(**kwargs):
    """Checks if the user has permitted operation `read`
    """
    if "handler" not in kwargs:
        return
    user = kwargs["handler"].get_current_user()
    username = user.get('name', '?')
    if kwargs["handler"].auth.is_permitted(
        username, Authorization.READ_OPERATION
    ):
        return True, username
    return False, username


class BaseHandler(HubOAuthenticated, web.RequestHandler):

    def set_default_headers(self) -> None:
        self.set_header("X-JupyterHub-Version", jupyterhub_version)
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        # prevent server fingerprinting
        self.clear_header('Server')


class StaticHandler(BaseHandler, web.StaticFileHandler):
    """A static handler that extends BaseHandler (for headers)."""


class MainHandler(BaseHandler):

    # hub_users = ["kinow"]
    # hub_groups = []
    # allow_admin = True

    def initialize(self, path, auth):
        self._static = path
        self.auth = auth

    @web.addslash
    @web.authenticated
    @read_authorised()
    def get(self):
        """Render the UI prototype."""
        index = os.path.join(self._static, "index.html")
        user = self.get_current_user()
        protocol = self.request.protocol
        host = self.request.host
        base_url = f'{protocol}://{host}/{user["server"]}'
        self.render(index, python_base_url=base_url)


class UserProfileHandler(BaseHandler):

    def initialize(self, auth):
        self.auth = auth

    def set_default_headers(self) -> None:
        super().set_default_headers()
        self.set_header("Content-Type", 'application/json')

    @web.authenticated
    @read_authorised()
    def get(self):
        user = self.get_current_user()
        user['perms'] = list(self.auth.get_permitted_operations(user['name']))
        self.write(json.dumps(user))


# This is needed in order to pass the server context in addition to existing.
# It's possible to just overwrite TornadoGraphQLHandler.context but we would
# somehow need to pass the request info (headers, username ...etc) in also
class UIServerGraphQLHandler(BaseHandler, TornadoGraphQLHandler):

    # No authorization decorators here, auth handled in AuthorizationMiddleware

    # Declare extra attributes
    resolvers = None

    def set_default_headers(self) -> None:
        self.set_header('Server', '')

    def initialize(self, schema=None, executor=None, middleware=None,
                   root_value=None, graphiql=False, pretty=False,
                   batch=False, backend=None, **kwargs):
        super(TornadoGraphQLHandler, self).initialize()

        self.auth = kwargs['auth']

        self.schema = schema
        if middleware is not None:
            self.middleware = list(self.instantiate_middleware(middleware))
        # Make authorization info available to auth middleware
        for mw in self.middleware:
            if isinstance(mw, AuthorizationMiddleware):
                mw.current_user = self.current_user['name']
                mw.auth = self.auth
        self.executor = executor
        self.root_value = root_value
        self.pretty = pretty
        self.graphiql = graphiql
        self.batch = batch
        self.backend = backend or get_default_backend()
        # Set extra attributes
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)

    @property
    def context(self):
        wider_context = {
            'graphql_params': self.graphql_params,
            'request': self.request,
            'resolvers': self.resolvers,
        }
        return wider_context

    async def execute(self, *args, **kwargs):
        return await self.schema.execute(
            *args,
            backend=self.backend,
            variable_values=kwargs.get('variables'),
            validate=False,
            **kwargs,
        )

    @web.authenticated
    async def post(self) -> None:
        try:
            await super().run("post")
        except Exception as ex:
            self.handle_error(ex)


class SubscriptionHandler(BaseHandler, websocket.WebSocketHandler):

    # No authorization decorators here, auth handled in AuthorizationMiddleware
    def initialize(self, sub_server, resolvers):
        self.queue = Queue(100)
        self.subscription_server = sub_server
        self.resolvers = resolvers
        if sub_server:
            self.subscription_server.current_user = self.current_user

    def select_subprotocol(self, subprotocols):
        return GRAPHQL_WS

    @websockets_authenticated
    def get(self, *args, **kwargs):
        return websocket.WebSocketHandler.get(self, *args, **kwargs)

    @websockets_authenticated  # noqa: A003 (open required)
    def open(self, *args, **kwargs):
        IOLoop.current().spawn_callback(self.subscription_server.handle, self,
                                        self.context)

    async def on_message(self, message):
        await self.queue.put(message)

    async def recv(self):
        return await self.queue.get()

    def recv_nowait(self):
        return self.queue.get_nowait()

    @property
    def context(self):
        wider_context = {
            'request': self.request,
            'resolvers': self.resolvers,
        }
        return wider_context


__all__ = [
    "MainHandler",
    "StaticHandler",
    "UserProfileHandler",
    "UIServerGraphQLHandler",
    "SubscriptionHandler"
]
