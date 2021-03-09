#!/usr/bin/env python3
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
from pathlib import Path
from typing import Any, Tuple, Type

from tornado import web, ioloop
from traitlets import (
    Unicode,
    default,
)
from traitlets.config import (
    Application
)

from cylc.flow.network.graphql import (
    CylcGraphQLBackend, IgnoreFieldMiddleware
)
from graphene_tornado.tornado_graphql_handler import TornadoGraphQLHandler
from jupyterhub.services.auth import HubOAuthCallbackHandler
from jupyterhub.utils import url_path_join

from cylc.uiserver import (
    __version__,
    __file__ as uis_pkg
)
from cylc.uiserver.config import __file__ as CONFIG_FILE
from .data_store_mgr import DataStoreMgr
from .handlers import (
    MainHandler,
    StaticHandler,
    SubscriptionHandler,
    UIServerGraphQLHandler,
    UserProfileHandler,
)
from .resolvers import Resolvers
from .schema import schema
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


class CylcUIServer(Application):

    ui_path = Unicode(config=True)

    @default('ui_path')
    def _dev_ui_path(self):
        return str(Path(uis_pkg).parents[3] / 'cylc-ui/dist')

    def __init__(self, port, jupyter_hub_service_prefix, static=None):
        self._load_uis_config()
        self._set_static_path(static)
        self._port = port
        self._jupyter_hub_service_prefix = jupyter_hub_service_prefix
        self.workflows_mgr = WorkflowsManager(self)
        self.data_store_mgr = DataStoreMgr(self.workflows_mgr)
        self.resolvers = Resolvers(
            self.data_store_mgr,
            workflows_mgr=self.workflows_mgr)

    def _load_uis_config(self):
        """Load the UIS config file."""
        # this environment variable enables loading of the config
        os.environ['CYLC_HUB_VERSION'] = __version__
        try:
            self.load_config_file(CONFIG_FILE)
        finally:
            del os.environ['CYLC_HUB_VERSION']
        # set traitlets values from the config
        for key, value in self.config.UIServer.items():
            print(f'# {key}={value}')
            setattr(self, key, value)

    def _set_static_path(self, static):
        """Set the path to static files.

        Args:
            static: Command line override of the ui_path traitlet.
        """
        if static:
            if os.path.isabs(static):
                self.ui_path = static
            else:
                script_dir = os.path.dirname(__file__)
                self.ui_path = os.path.abspath(os.path.join(
                    script_dir,
                    static
                ))

    def _create_static_handler(
            self,
            path: str
    ) -> Tuple[str, Type[StaticHandler], dict]:
        """
        Create a static content handler.

        Args:
            path (str): handler path (supports regular expressions)
        Returns:
            Tornado handler tuple
        """
        return (
            rf"{self._jupyter_hub_service_prefix}({path})",
            StaticHandler,
            {"path": self.ui_path}
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
        logger.info(self.ui_path)
        # subscription/websockets server
        subscription_server = TornadoSubscriptionServer(
            schema,
            backend=CylcGraphQLBackend(),
            middleware=[IgnoreFieldMiddleware],
        )
        return MyApplication(
            static_path=self.ui_path,
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
                # subscription/websockets handler
                self._create_handler("subscriptions",
                                     SubscriptionHandler,
                                     sub_server=subscription_server,
                                     resolvers=self.resolvers),
                # main handler
                (
                    rf"{self._jupyter_hub_service_prefix}?",
                    MainHandler,
                    {"path": self.ui_path}
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
            self.workflows_mgr.update)
        # If the client is already established it's not overridden,
        # so the following callbacks can happen at the same time.
        ioloop.PeriodicCallback(
            self.workflows_mgr.update, 5000).start()
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
    parser.add_argument('-s', '--static', action="store", dest="static")
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


__all__ = [
    'MyApplication',
    'CylcUIServer',
    'main'
]
