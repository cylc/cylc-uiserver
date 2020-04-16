#!/usr/bin/env python3

# -*- coding: utf-8 -*-
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

import argparse
import json
import logging
import os
import signal
from functools import partial
from logging.config import dictConfig
from os.path import join, abspath, dirname
from typing import Any, Tuple, Type

from tornado import web, ioloop

from cylc.flow.network.graphql import (
    CylcGraphQLBackend, IgnoreFieldMiddleware
)
from cylc.flow.network.schema import schema
from graphene_tornado.tornado_graphql_handler import TornadoGraphQLHandler
from jupyterhub.services.auth import HubOAuthCallbackHandler
from jupyterhub.utils import url_path_join
from .data_store_mgr import DataStoreMgr
from .handlers import *
from .resolvers import Resolvers
from .websockets.tornado import TornadoSubscriptionServer
from .workflows_mgr import WorkflowsManager

logger = logging.getLogger(__name__)


class MyApplication(web.Application):
    is_closing = False

    def signal_handler(self, signum, frame):
        logger.info('exiting...')
        self.is_closing = True

    def try_exit(self, uis):
        # clean up and stop in here
        if self.is_closing:
            # stop the subscribers running in the thread pool executor
            for sub in uis.data_store_mgr.w_subs.values():
                sub.stop()
            # Shutdown the thread pool executor
            for executor in uis.data_store_mgr.executors.values():
                executor.shutdown(wait=False)
            # Destroy ZeroMQ context of all sockets
            uis.workflows_mgr.context.destroy()
            ioloop.IOLoop.instance().stop()
            logger.info('exit success')


class CylcUIServer(object):

    def __init__(self, port, static, jupyter_hub_service_prefix):
        self._port = port
        if os.path.isabs(static):
            self._static = static
        else:
            script_dir = os.path.dirname(__file__)
            self._static = os.path.abspath(os.path.join(script_dir, static))
        self._jupyter_hub_service_prefix = jupyter_hub_service_prefix
        self.workflows_mgr = WorkflowsManager(self)
        self.data_store_mgr = DataStoreMgr(self.workflows_mgr)
        self.resolvers = Resolvers(
            self.data_store_mgr,
            workflows_mgr=self.workflows_mgr)

    def _create_static_handler(
            self,
            path: str
    ) -> Tuple[str, Type[web.StaticFileHandler], dict]:
        """
        Create a static content handler.

        Args:
            path (str): handler path (supports regular expressions)
        Returns:
            Tornado handler tuple
        """
        return (
            rf"{self._jupyter_hub_service_prefix}({path})",
            web.StaticFileHandler,
            {"path": self._static}
        )

    def _create_handler(
            self,
            path: str,
            clazz: Type[web.RequestHandler],
            **kwargs: Any
    ) -> Tuple[str, Type[web.RequestHandler], dict]:
        """
        Create a Tornado handler.

        Args:
            path (str): handler path
            clazz (class): handler class
            kwargs: extra params
        Returns:
            Tornado handler tuple
        """
        return (
            url_path_join(self._jupyter_hub_service_prefix, path),
            clazz,
            kwargs
        )

    def _create_graphql_handler(
            self,
            path: str,
            clazz: Type[TornadoGraphQLHandler],
            **kwargs: Any
    ) -> Tuple[str, Type[web.RequestHandler], dict]:
        """
        Create a GraphQL handler.

        Args:
            path (str): handler path
            clazz (class): handler class
            kwargs: extra params
        Returns:
            Tornado handler tuple
        """
        return self._create_handler(
            path,
            clazz,
            schema=schema,
            resolvers=self.resolvers,
            backend=CylcGraphQLBackend(),
            middleware=[IgnoreFieldMiddleware],
            **kwargs
        )

    def _make_app(self, debug: bool):
        """Crete a Tornado web application.

        Args:
            debug (bool): flag to set debugging in the Tornado application
        """
        logger.info(self._static)
        # subscription/websockets server
        subscription_server = TornadoSubscriptionServer(
            schema,
            backend=CylcGraphQLBackend(),
            middleware=[IgnoreFieldMiddleware],
        )
        return MyApplication(
            static_path=self._static,
            debug=debug,
            handlers=[
                # static content
                self._create_static_handler(".*.(css|js)"),
                self._create_static_handler("(fonts|img)/.*"),
                self._create_static_handler("favicon.png"),
                # normal handlers, with auth
                self._create_handler("oauth_callback",
                                     HubOAuthCallbackHandler),
                self._create_handler("userprofile",
                                     UserProfileHandler),
                # graphql handlers
                self._create_graphql_handler(
                    "graphql",
                    UIServerGraphQLHandler,
                ),
                self._create_graphql_handler(
                    "graphql/batch",
                    UIServerGraphQLHandler,
                    batch=True
                ),
                self._create_graphql_handler(
                    "graphql/graphiql",
                    GraphiQLHandler,
                    graphiql=True
                ),
                # subscription/websockets handler
                self._create_handler("subscriptions",
                                     SubscriptionHandler,
                                     sub_server=subscription_server,
                                     resolvers=self.resolvers),
                # main handler
                (
                    rf"{self._jupyter_hub_service_prefix}?",
                    MainHandler,
                    {"path": self._static}
                )
            ],
            # always generate a new cookie secret on launch
            # ensures that each spawn clears any cookies from
            # previous session, triggering OAuth again
            cookie_secret=os.urandom(32)
        )

    def start(self, debug: bool):
        app = self._make_app(debug)
        signal.signal(signal.SIGINT, app.signal_handler)
        app.listen(self._port)
        # pass in server object for clean exit
        ioloop.PeriodicCallback(
            partial(app.try_exit, uis=self), 100).start()
        # Discover workflows on initial start up.
        ioloop.IOLoop.current().add_callback(
            self.workflows_mgr.gather_workflows)
        # If the client is already established it's not overridden,
        # so the following callbacks can happen at the same time.
        ioloop.PeriodicCallback(
            self.workflows_mgr.gather_workflows, 7000).start()
        try:
            ioloop.IOLoop.current().start()
        except KeyboardInterrupt:
            ioloop.IOLoop.instance().stop()


def main():
    parser = argparse.ArgumentParser(
        description="Start Cylc UI"
    )
    parser.add_argument('-p', '--port', action="store", dest="port", type=int,
                        default=8888)
    parser.add_argument('-s', '--static', action="store", dest="static",
                        required=True)
    parser.add_argument('--debug', action="store_true", dest="debug",
                        default=False)
    here = abspath(dirname(__file__))
    parser.add_argument('--logging-config', type=argparse.FileType('r'),
                        help='path to logging configuration file',
                        action="store", dest="logging_config",
                        default=join(here, 'logging_config.json'))
    args = parser.parse_known_args()[0]

    # args.logging_config will be a io.TextIOWrapper resource
    with args.logging_config as logging_config_json:
        config = json.load(logging_config_json)
        dictConfig(config["logging"])

    jupyterhub_service_prefix = os.environ.get(
        'JUPYTERHUB_SERVICE_PREFIX', '/')
    logger.info(f"JupyterHub Service Prefix: {jupyterhub_service_prefix}")
    ui_server = CylcUIServer(
        port=args.port,
        static=args.static,
        jupyter_hub_service_prefix=jupyterhub_service_prefix
    )
    logger.info(f"Listening on {args.port} and serving static content from "
                f"{args.static}")

    logger.info("Starting Cylc UI")
    ui_server.start(args.debug)


if __name__ == "__main__":
    main()


__all__ = [
    'MyApplication',
    'CylcUIServer',
    'main'
]
