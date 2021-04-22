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
from functools import partial

from .websockets import authenticated as websockets_authenticated

logger = logging.getLogger(__name__)


ME = getpass.getuser()

# TODO: Remove this auth code into an authorise.py file for tidiness.


def _authorised(req):
    """Authorise a request.

    Requires the request to be authenticated.

    Currently returns True if the authenticated user is the same as the
    user under which this UI Server is running.

    Returns:
        bool - True if the request passes authorisation, False if it fails.
"""
# 1. Send roles and/or claims/actions (see oauth/jwt for 'claims' concept)
# 2. Lookup roles and/or actions in cylc config get all USERS and GROUPS
# 3. Get groups for current user
# 4. See if username or groups for current user are in those returned in (2)
#
# e.g.
#
# @authorise(roles="users,admins", claims="can_load_ui")
#
# Eventually you can nest i.e. add one role to another
#
# e.g.
#
# admins group could be a member of users group to INHERIT perms.
# and save repeating


CAN_READ = "readers"
CAN_WRITE = "writers"
CAN_EXECUTE = "executers"

MEMBERTYPE_GROUP = "group"
MEMBERTYPE_USERNAME = "username"

# TODO Fake until we plumb in config
# c.UIServer.authorisation = {
#     "user_A": {
#         "read": True,
#        "write": [
#             "pause"
#         ]
#     },
#     "group:users": {
#         "read": True
#     }
# }

roles_dict = {CAN_READ: [{MEMBERTYPE_USERNAME: "mhall"}, {
    MEMBERTYPE_USERNAME: "testuser1"}, {
    MEMBERTYPE_GROUP: "users"}],
    CAN_WRITE: [{MEMBERTYPE_USERNAME: "mhall"}, {
        MEMBERTYPE_GROUP: "users"}],
    CAN_EXECUTE: [{MEMBERTYPE_USERNAME: "mhall"}, {
                  MEMBERTYPE_GROUP: "users"}]}


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


def _user_action_allowed(username, action):
    for role in roles_dict[action]:
        roleuser = role.get(MEMBERTYPE_USERNAME)
        if roleuser and roleuser == username:
            return True
    # There's a number of ways to find groups but this is the only way
    # to include non-local-machine groups while targeting a specific user.
    # Requires a gid so supply 0 or some 'max integer' and remove from result
    # see https://www.geeksforgeeks.org/python-os-getgrouplist-method/
    group_ids = os.getgrouplist(username, 0)
    group_ids.remove(0)
    users_groups = list(map(lambda x: grp.getgrgid(x).gr_name, group_ids))
    for role in roles_dict[action]:
        rolegroup = role.get(MEMBERTYPE_GROUP)
        if rolegroup and rolegroup in users_groups:
            return True

# TODO look to refactor can_* into a single function
#
# e.g.
#
# back to authorise decorator function that takes:
# authorise(can_read)
# which can be the function needed to do the checks


def can_read(fun):
    if iscoroutinefunction(fun):
        async def _inner(self, *args, **kwargs):
            allowed, username = _can_read(self)
            if not allowed:
                logger.warn(f'Authorisation failed for {username}')
                raise web.HTTPError(403)
            return await fun(self, *args, **kwargs)
        return _inner
    else:
        def _inner(self, *args, **kwargs):
            allowed, username = _can_read(self)
            if not allowed:
                logger.warn(f'Authorisation failed for {username}')
                raise web.HTTPError(403)
            return fun(self, *args, **kwargs)
        return _inner


# TUESDAY TODO: fish the mutation operation_name out of args to make this work
def can_execute(fun):
    """Provides Cylc authorisation for multi-user setups."""
    if asyncio.iscoroutinefunction(fun):


def _can_read(self):
    user = self.get_current_user()

def authorise(*outer_args, **outer_kwargs):
    def authorise_inner(fun):
        if iscoroutinefunction(fun):
            async def decorated_func(self, *args, **kwargs):
                for function in outer_args:
                    if callable(function):
                        allowed, username = function(handler=self)
                    if not allowed:
                        logger.warn(f'Authorisation failed for {username}')
                        raise web.HTTPError(403)
                return await fun(self, *args, **kwargs)
            return decorated_func
        else:
            def decorated_func(self):
                for function in outer_args:
                    # todo raise / log
                    if callable(function):
                        allowed, username = function(handler=self)
                    if not allowed:
                        logger.warn(f'Authorisation failed for {username}')
                        raise web.HTTPError(403)
                return fun(self)
            return decorated_func
    return authorise_inner


def can_read(**kwargs):
    if "handler" not in kwargs:
        return
    user = kwargs["handler"].get_current_user()
    username = user.get('name', '?')
    if username == ME or _user_action_allowed(username, "readers"):
        return True, username
    return False, username


def can_write(**kwargs):
    if "handler" not in kwargs:
        return
    user = kwargs["handler"].get_current_user()
    username = user.get('name', '?')
    if username == ME or _user_action_allowed(username, "writers"):
        return True, username
    return False, username


def can_execute(**kwargs):
    if "handler" not in kwargs or "mutators" not in kwargs:
        return
    handler = kwargs["handler"]
    mutators = kwargs["mutators"]
    user = handler.get_current_user()
    username = user.get('name', '?')

    if username == ME:
        return True, username

    # TODO Should also check the query e.g. it starts with 'mutation pause'
    # For security in case an operation name is sent different to the query
    # Hence fetching below

    # TODO decide on behaviour where @can_execute without any mutators
    # Probably will mean all mutators needs execute?
    # Same goes for where operation_name is missing as per first call
    # Currently treating as if present below
    # Main aim = fail secure

    if isinstance(handler, TornadoGraphQLHandler) and mutators is not None:
        operation_name, query = _get_graphql_operation(handler)
        if operation_name in mutators or operation_name is None:
            if _user_action_allowed(username, CAN_EXECUTE):
                return True, username
    return False, username


def _get_graphql_operation(req):
    data = req.parse_body()
    query, _, operation_name, _ = req.get_graphql_params(
                req.request, data)
    return operation_name, query


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

    def initialize(self, path):
        self._static = path

    @web.addslash
    @web.authenticated
    @authorise(can_read)
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
    @authorise(can_read)
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
    @authorise(can_write,
               partial(can_execute, mutators=["play", "stop"]))
    async def post(self) -> None:
        try:
            await super().run("post")
        except Exception as ex:
            self.handle_error(ex)


class SubscriptionHandler(BaseHandler, websocket.WebSocketHandler):

    def initialize(self, sub_server, resolvers, user_auth_config):
        self.queue = Queue(100)
        self.subscription_server = sub_server
        self.resolvers = resolvers
        self.user_auth_config = user_auth_config

    def select_subprotocol(self, subprotocols):
        return GRAPHQL_WS

    @websockets_authenticated
    @authorise(can_read)
    def get(self, *args, **kwargs):
        # forward this call so we can authenticate/authorise it
        return websocket.WebSocketHandler.get(self, *args, **kwargs)

    @websockets_authenticated
    @authorise(can_read)
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
