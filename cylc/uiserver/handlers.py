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
from asyncio import Queue
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


logger = logging.getLogger(__name__)


ME = getpass.getuser()


def _authorised(req):
    """Authorise a request.

    Requires the request to be authenticated.

    Currently returns True if the authenticated user is the same as the
    user under which this UI Server is running.

    Returns:
        bool - True if the request passes authorisation, False if it fails.

    """
    user = req.get_current_user()
    username = user.get('name', '?')
    if username != ME:
        logger.warning(f'Authorisation failed for {username}')
        return False
    return True


def authorised(fun):
    """Provides Cylc authorisation for multi-user setups."""

    def _inner(self, *args, **kwargs):
        nonlocal fun
        if not _authorised(self):
            raise web.HTTPError(403, reason='authorisation insufficient')
        return fun(self, *args, **kwargs)
    return _inner


def async_authorised(fun):
    """Provides Cylc authorisation for multi-user setups."""

    async def _inner(self, *args, **kwargs):
        nonlocal fun
        if not _authorised(self):
            raise web.HTTPError(403, reason='authorisation insufficient')
        return await fun(self, *args, **kwargs)
    return _inner


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

    def initialize(self, path):
        self._static = path

    @web.addslash
    @web.authenticated
    @authorised
    def get(self):
        """Render the UI prototype."""
        index = os.path.join(self._static, "index.html")
        user = self.get_current_user()
        protocol = self.request.protocol
        host = self.request.host
        base_url = f'{protocol}://{host}/{user["server"]}'
        self.render(index, python_base_url=base_url)


class UserProfileHandler(BaseHandler):

    def set_default_headers(self) -> None:
        super().set_default_headers()
        self.set_header("Content-Type", 'application/json')

    @web.authenticated
    @authorised
    def get(self):
        self.write(json.dumps(self.get_current_user()))


# This is needed in order to pass the server context in addition to existing.
# It's possible to just overwrite TornadoGraphQLHandler.context but we would
# somehow need to pass the request info (headers, username ...etc) in also
class UIServerGraphQLHandler(BaseHandler, TornadoGraphQLHandler):

    # Declare extra attributes
    resolvers = None

    def set_default_headers(self) -> None:
        self.set_header('Server', '')

    def initialize(self, schema=None, executor=None, middleware=None,
                   root_value=None, graphiql=False, pretty=False,
                   batch=False, backend=None, **kwargs):
        super(TornadoGraphQLHandler, self).initialize()

        self.schema = schema
        if middleware is not None:
            self.middleware = list(self.instantiate_middleware(middleware))
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

    @web.authenticated
    @authorised
    def prepare(self):
        super().prepare()

    @web.authenticated
    @async_authorised
    async def execute(self, *args, **kwargs):
        # Use own backend, and TornadoGraphQLHandler already does validation.
        return await self.schema.execute(
            *args,
            backend=self.backend,
            variable_values=kwargs.get('variables'),
            validate=False,
            **kwargs,
        )

    @web.authenticated
    @async_authorised
    async def run(self, *args, **kwargs):
        await TornadoGraphQLHandler.run(self, *args, **kwargs)


class SubscriptionHandler(BaseHandler, websocket.WebSocketHandler):

    def initialize(self, sub_server, resolvers):
        self.queue = Queue(100)
        self.subscription_server = sub_server
        self.resolvers = resolvers

    def select_subprotocol(self, subprotocols):
        return GRAPHQL_WS

    @websockets_authenticated
    @authorised
    def get(self, *args, **kwargs):
        # forward this call so we can authenticate/authorise it
        return websocket.WebSocketHandler.get(self, *args, **kwargs)

    @websockets_authenticated
    @authorised
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
