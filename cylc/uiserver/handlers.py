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
from functools import wraps
import json
import getpass
import socket
from typing import Callable, Union

from graphene_tornado.tornado_graphql_handler import TornadoGraphQLHandler
from graphql import get_default_backend
from graphql_ws.constants import GRAPHQL_WS
from jupyter_server.base.handlers import JupyterHandler
from tornado import web, websocket
from tornado.ioloop import IOLoop

from cylc.flow.scripts.cylc import (
    get_version as get_cylc_version,
    list_plugins as list_cylc_plugins,
)

from cylc.uiserver.authorise import AuthorizationMiddleware
from cylc.uiserver.websockets import authenticated as websockets_authenticated


ME = getpass.getuser()




def authorised(fun: Callable) -> Callable:
    """Provides Cylc authorisation.

    When the UIS is run standalone (token-authenticated) application,
    authorisation is deactivated, the bearer of the token has full privileges.

    When the UIS is spawned by Jupyter Hub (hub authenticated), multi-user
    access is permitted. Users are authorised by _authorise.
    """

    @wraps(fun)
    def _inner(
        handler: 'CylcAppHandler',
        *args,
        **kwargs,
    ):
        nonlocal fun
        user: Union[
            None,   # unauthenticated
            dict,   # hub auth
            str,    # token auth or anonymous

        ] = handler.get_current_user()
        if user is None or user == 'anonymous':
            # user is not authenticated - calls should not get this far
            # but the extra safety doesn't hurt
            # NOTE: Auth tests will hit this line unless mocked authentication
            # is provided.
            raise web.HTTPError(403, reason='Forbidden')
        if not (
            isinstance(user, str)  # token authenticated
            or (
                isinstance(user, dict)
                and _authorise(handler, user['name'], '')
            )
        ):
            raise web.HTTPError(403, reason='authorisation insufficient')
        return fun(handler, *args, **kwargs)
    return _inner


def is_token_authenticated(
    handler: JupyterHandler,
    user: Union[bytes, dict, str],
) -> bool:
    """Returns True if the UIS is running "standalone".

    At present we cannot use handler.is_token_authenticated because it
    returns False when the token is cached in a cookie.

    https://github.com/jupyter-server/jupyter_server/pull/562
    """
    if isinstance(user, bytes):  # noqa: SIM114
        # Cookie authentication:
        # * The URL token is added to a secure cookie, it can then be
        #   removed from the URL for subsequent requests, the cookie is
        #   used in its place.
        # * If the token was used token_authenticated is True.
        # * If the cookie was used it is False (despite the cookie auth
        #   being derived from token auth).
        # * Due to a bug in jupyter_server the user is returned as bytes
        #   when cookie auth is used so at present we can use this to
        #   tell.
        #   https://github.com/jupyter-server/jupyter_server/pull/562
        # TODO: this hack is obviously not suitable for production!
        return True
    elif handler.token_authenticated:
        # standalone UIS, the bearer of the token is the owner
        # (no multi-user functionality so no further auth required)
        return True
    return False


def _authorise(
    handler: 'CylcAppHandler',
    username: str,
    action: str = 'READ'
) -> bool:
    """Authorises a user to perform an action.

    Currently this returns False unless the authenticated user is the same
    as the user this server is running under.
    """
    if username != ME:
        # auth provided by the hub, check the user name
        handler.log.warning(f'Authorisation failed for {username}')
        return False
    return True


class CylcAppHandler(JupyterHandler):
    """Base handler for Cylc endpoints.

    This handler adds the Cylc authorisation layer which is triggered by
    calling CylcAppHandler.get_current_user which is called by
    web.authenticated.

    When running as a Hub application the make_singleuser_app method patches
    this handler to insert the HubOAuthenticated bases class high up
    in the inheritance order.

    https://github.com/jupyterhub/jupyterhub/blob/
    3800ceaf9edf33a0171922b93ea3d94f87aa8d91/jupyterhub/
    singleuser/mixins.py#L826
    """

    auth_level = None

    @property
    def hub_users(self):
        # allow all users (handled by Cylc authorisation decorator)
        return None

    @property
    def hub_groups(self):
        # allow all groups (handled by Cylc authorisation decorator)
        return None


class CylcStaticHandler(CylcAppHandler, web.StaticFileHandler):
    """Serves the Cylc UI static files.

    Jupyter Server provides a way of serving Jinja2 templates / static files,
    however, this does not work for us because:

    * Our static files live in subdirectories which Jupyter Server does not
      support.
    * Our UI expects to find its resources under the same URL, i.e. we
      aren't using Jinja2 to inject the static path.
    * We need to push requests through CylcAppHandler in order to allow
      multi-user access.
    """

    @web.authenticated
    def get(self, path):
        # authenticate the static handler
        # this provides us with login redirection and token cashing
        return web.StaticFileHandler.get(self, path)


class CylcVersionHandler(CylcAppHandler):
    """Renders information about the Cylc environment.

    Equivalent to running `cylc version --long` in the UIS environment.
    """

    @authorised
    @web.authenticated
    def get(self):
        self.write(
            '<pre>'
            + get_cylc_version(long=True)
            + '\n'
            + list_cylc_plugins()
            + '</pre>'
        )


class UserProfileHandler(CylcAppHandler):
    """Provides information about the user in JSON format.

    When running via the hub this returns the hub user information.

    When running standalone we provide something similar to what the hub
    would have returned.
    """

    def set_default_headers(self) -> None:
        super().set_default_headers()
        self.set_header("Content-Type", 'application/json')

    @authorised
    def get(self):
        user_info = self.get_current_user()

        if isinstance(user_info, dict):
            # the server is running with authentication services provided
            # by a hub
            user_info = dict(user_info)  # make a copy for safety
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


class UIServerGraphQLHandler(CylcAppHandler, TornadoGraphQLHandler):
    """Endpoint for performing GraphQL queries.

    This is needed in order to pass the server context in addition to existing.
    It's possible to just overwrite TornadoGraphQLHandler.context but we would
    somehow need to pass the request info (headers, username ...etc) in also
    """

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
        current_user = self.get_current_user()
        if isinstance(current_user, dict):
            # the server is running with authentication services provided
            # by a hub
            current_user = dict(current_user)  # make a copy for safety
        else:
            # the server is running using a token
            # authentication is provided by jupyter server
            current_user = {
                'kind': 'user',
                'name': ME,
                'server': socket.gethostname()
            }

        if middleware is not None:
            self.middleware = list(self.instantiate_middleware(middleware))
        # Make authorization info available to auth middleware
        for mw in self.middleware:
            if isinstance(mw, AuthorizationMiddleware):
                mw.current_user = current_user['name']
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
    """Endpoint for performing GraphQL subscriptions."""
    # No authorization decorators here, auth handled in AuthorizationMiddleware
    def initialize(self, sub_server, resolvers):
        self.queue = Queue(100)
        self.subscription_server = sub_server
        self.resolvers = resolvers
        if sub_server:
            self.subscription_server.current_user = self.get_current_user()

    def select_subprotocol(self, subprotocols):
        return GRAPHQL_WS

    @websockets_authenticated
    def get(self, *args, **kwargs):
        # forward this call so we can authenticate/authorise it
        return websocket.WebSocketHandler.get(self, *args, **kwargs)

    @websockets_authenticated  # noqa: A003
    def open(self, *args, **kwargs):  # noqa: A003
        IOLoop.current().spawn_callback(
            self.subscription_server.handle,
            self,
            self.context,
        )

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
