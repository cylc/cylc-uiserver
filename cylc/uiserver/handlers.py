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

from asyncio import Queue
import json
import os
import logging
import getpass
import socket

from graphene_tornado.tornado_graphql_handler import TornadoGraphQLHandler
from graphql import get_default_backend
from graphql_ws.constants import GRAPHQL_WS
from jupyter_server.base.handlers import JupyterHandler
from jupyterhub import __version__ as jupyterhub_version
from jupyterhub.services.auth import HubOAuthenticated
from jupyterhub.utils import url_path_join
from tornado import web, websocket
from tornado.ioloop import IOLoop

from .websockets import authenticated as websockets_authenticated


ME = getpass.getuser()


# def _authorised(req):
#     """Authorise a request.

#     Requires the request to be authenticated.

#     Currently returns True if the authenticated user is the same as the
#     user under which this UI Server is running.

#     Returns:
#         bool - True if the request passes authorisation, False if it fails.

#     """
#     return True  # TODO
#     # jupyter server has a method to get the user from a token
#     # https://github.com/jupyter-server/jupyter_server/blob/ca5622a0706f60f299881adc45e2f7e94045ca22/jupyter_server/auth/login.py#L197
#     user = req.get_current_user()
#     username = user.get('name', '?')
#     if username != ME:
#         logger.warning(f'Authorisation failed for {username}')
#         return False
#     return True


# def authorised(fun):
#     """Provides Cylc authorisation for multi-user setups."""

#     def _inner(self, *args, **kwargs):
#         nonlocal fun
#         if not _authorised(self):
#             raise web.HTTPError(403, reason='authorisation insufficient')
#         return fun(self, *args, **kwargs)
#     return _inner


# def async_authorised(fun):
#     """Provides Cylc authorisation for multi-user setups."""

#     async def _inner(self, *args, **kwargs):
#         nonlocal fun
#         if not _authorised(self):
#             raise web.HTTPError(403, reason='authorisation insufficient')
#         return await fun(self, *args, **kwargs)
#     return _inner


# CylcAppHandler = JupyterHandler



class CylcAppHandler(JupyterHandler):
    """Base handler for Cylc endpoints.

    This handler adds the Cylc authorisation layer which is triggered by
    calling CylcAppHandler.get_current_user which is called by web.authenticated.

    When running as a Hub application the make_singleuser_app method patches
    this handler to insert the HubOAuthenticated bases class high up
    in the inheritance order.

    https://github.com/jupyterhub/jupyterhub/blob/
    2c8b29b6bbd7197f34f553668365dbe16d001f03/
    jupyterhub/singleuser/mixins.py#L716

    TODO:
        * Implement authorisation!!!
        * Make authorisation configurabe via this class.
        * Make properties traitlets.

    """

    auth_level = None

    @property
    def hub_users(self):
        # allow all users (handled by authorisation)
        return None

    @property
    def hub_groups(self):
        # allow all groups (handled by authorisation)
        return None

    def get_current_user(self):
        user = CylcAppHandler.__bases__[0].get_current_user(self)
        self.authorise(user)
        return user

    def authorise(self, user):
        if not self._authorise(user):
            raise web.HTTPError(403, reason='authorisation insufficient')

    def _authorise(self, user):
        self.log.debug(f'authorise {user} for {self.__class__}')
        return True
        # if user != ME:
        #     self.log.warning(f'Authorisation failed for {user}')
        #     return False
        # return True


# class CylcAppHandler(HubOAuthenticated, web.RequestHandler):

#     def set_default_headers(self) -> None:
#         self.set_header("X-JupyterHub-Version", jupyterhub_version)
#         self.set_header("Access-Control-Allow-Origin", "*")
#         self.set_header("Access-Control-Allow-Headers", "x-requested-with")
#         self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
#         # prevent server fingerprinting
#         self.clear_header('Server')
#         print(f'%%% {self.request}')

class StaticHandler2(web.StaticFileHandler):

    def get(self, *args, **kwargs):
        # args = (args[0].replace('cylc/', ''),)
        super().get(*args, **kwargs)


class StaticHandler(CylcAppHandler, web.StaticFileHandler):
    """A static handler that extends CylcAppHandler (for headers)."""


class MainHandler(CylcAppHandler):

    def initialize(self, path):
        self._static = path

    @web.addslash
    @web.authenticated
    def get(self):
        """Render the UI prototype."""
        index = os.path.join(self._static, "index.html")
        user = self.get_current_user()
        protocol = self.request.protocol
        host = self.request.host
        base_url = f'{protocol}://{host}/{user["server"]}'
        self.render(index, python_base_url=base_url)


class UserProfileHandler(CylcAppHandler):

    def set_default_headers(self) -> None:
        super().set_default_headers()
        self.set_header("Content-Type", 'application/json')

    @web.authenticated
    def get(self):
        user_info = self.get_current_user()

        if isinstance(user_info, dict):
            # the server is running with authentication services provided
            # by a hub
            pass
        else:
            # the server is running using a token
            # authentication is provided by jupyter server
            user_info = {
                'kind': 'user',
                'name': ME,
                'server': socket.gethostname()
            }

        # add an entry for the workflow owner
        # NOTE: when running behind a hub this may be different from the
        # authenticated user
        user_info['owner'] = ME

        self.write(json.dumps(user_info))


# This is needed in order to pass the server context in addition to existing.
# It's possible to just overwrite TornadoGraphQLHandler.context but we would
# somehow need to pass the request info (headers, username ...etc) in also
class UIServerGraphQLHandler(CylcAppHandler, TornadoGraphQLHandler):

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
    def prepare(self):
        super().prepare()

    @web.authenticated
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
    async def run(self, *args, **kwargs):
        await TornadoGraphQLHandler.run(self, *args, **kwargs)


class SubscriptionHandler(CylcAppHandler, websocket.WebSocketHandler):

    def initialize(self, sub_server, resolvers):
        self.queue = Queue(100)
        self.subscription_server = sub_server
        self.resolvers = resolvers

    def select_subprotocol(self, subprotocols):
        return GRAPHQL_WS

    @websockets_authenticated
    def get(self, *args, **kwargs):
        # forward this call so we can authenticate/authorise it
        return websocket.WebSocketHandler.get(self, *args, **kwargs)

    @websockets_authenticated
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
