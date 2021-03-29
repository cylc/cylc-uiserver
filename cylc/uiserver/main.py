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
from contextlib import contextmanager
import json
import logging
import os
import signal
from functools import partial
from logging.config import dictConfig
from pathlib import Path, PurePath
import sys
from typing import Any, Tuple, Type, List

from pkg_resources import parse_version
from tornado import web, ioloop
from traitlets import (
    Float,
    TraitError,
    TraitType,
    Undefined,
    Unicode,
    default,
    validate,
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


class PathType(TraitType):
    """A pathlib traitlet type which allows string and undefined values."""

    @property
    def info_text(self):
        return 'a pathlib.PurePath object'

    def validate(self, obj, value):
        if isinstance(value, str):
            return Path(value).expanduser()
        if isinstance(value, PurePath):
            return value
        if value == Undefined:
            return value
        self.error(obj, value)


class CylcUIServer(Application):

    ui_path = PathType(
        config=False,
        help='''
            Path to the UI build to serve.

            Internal config derived from ui_build_dir and ui_version.
        '''
    )
    ui_build_dir = PathType(
        config=True,
        help='''
            The directory containing the UI build.

            This can be a directory containing a single UI build e.g::

               dir/
                   index.html

            Or a tree of builds where each build has a version number e.g::

               dir/
                   1.0/
                       index.html
                   2.0/
                       index.html

            By default this points at the UI build tree which was bundled with
            the UI Server. Change this if you want to pick up a different
            build e.g. for development or evaluation purposes.

            Takes effect on (re)start.
        '''
    )
    ui_version = Unicode(
        config=True,
        help='''
            Hardcodes the UI version to serve.

            If the ``ui_build_dir`` is a tree of builds, this config can be
            used to determine which UI build is used.

            By default the highest version is chosen according to PEP440
            version sorting rules.

            Takes effect on (re)start.
        '''
    )
    logging_config = PathType(
        config=True,
        help='''
            Set the path to a logging config JSON file.

            This configures what gets logged where.

            For more information on logging configuration see:
            https://docs.python.org/3/library/logging.config.html

            Currently only JSON format is supported.

            If unspecified the default config located in
            ``cylc/uiserver/logging_config.json`` will apply.
        '''
    )
    scan_interval = Float(
        config=True,
        help='''
            Set the interval between workflow scans in seconds.

            Workflow scans allow a UI server to detect workflows which have
            been started from the CLI since the last update.

            This involves a number of filesystem operations, to reduce
            system load set a higher value.
        '''
    )

    @default('scan_interval')
    def _default_scan_interval(self):
        return 5

    @validate('ui_build_dir')
    def _check_ui_build_dir_exists(self, proposed):
        if proposed['value'].exists():
            return proposed['value']
        raise TraitError(f'ui_build_dir does not exist: {proposed["value"]}')

    @staticmethod
    def _list_ui_versions(path: Path) -> List[str]:
        """Return a list of UI build versions detected in self.ui_path."""
        return list(
            sorted(
                (
                    version.name
                    for version in path.glob('[0-9][0-9.]*')
                    if version
                ),
                key=parse_version
            )
        )

    @default('ui_path')
    def _get_ui_path(self):
        build_dir = self.ui_build_dir
        version = self.ui_version

        if build_dir and build_dir != Undefined:
            # ui path has been configured, check if the path is a build
            # (rather than a dir of builds e.g. development build)
            if (build_dir / 'index.html').exists():
                return build_dir
        else:
            # default UI build base directory
            build_dir = Path(uis_pkg).parent / 'ui'

        if not version:
            # pick the highest installed version by default
            try:
                version = self._list_ui_versions(build_dir)[-1]
            except IndexError:
                raise Exception(
                    f'Could not find any UI builds in {build_dir}.'
                )

        ui_path = build_dir / version
        if (ui_path / 'index.html').exists():
            return ui_path

        raise Exception(f'Could not find UI build in {ui_path}')

    @default('logging_config')
    def _default_logging_config(self):
        return Path(Path(uis_pkg).parent / 'logging_config.json')

    def __init__(self, port, jupyterhub_service_prefix, ui_build_dir=None):
        with self._interim_log():
            self._load_uis_config()
            self._open_log()
        if ui_build_dir:
            self.ui_build_dir = Path(ui_build_dir)
        self._port = port
        self._jupyter_hub_service_prefix = jupyterhub_service_prefix
        self.workflows_mgr = WorkflowsManager(self)
        self.data_store_mgr = DataStoreMgr(self.workflows_mgr)
        self.resolvers = Resolvers(
            self.data_store_mgr,
            workflows_mgr=self.workflows_mgr)

    @staticmethod
    @contextmanager
    def _interim_log():
        """Capture log messages before the logging config has been processed.

        The logging configuration is configured via the configuration file
        which means we can't configure logging until we have loaded the
        configuration. Any log output in the interim would be lost so we
        use a temporary handler to record it to the console.
        """
        log = logging.getLogger()
        handler = logging.StreamHandler(stream=sys.stdout)
        log.setLevel(logging.DEBUG)
        handler.setLevel(logging.DEBUG)
        log.addHandler(handler)
        yield
        log.removeHandler(handler)

    def _open_log(self):
        """Configure logging and open log handler(s)."""
        if self.logging_config:
            if self.logging_config.exists():
                with open(self.logging_config, 'r') as logging_config_json:
                    config = json.load(logging_config_json)
                    dictConfig(config["logging"])
            else:
                raise ValueError(
                    f'Logging config file not found: {self.logging_config}'
                )

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
            setattr(self, key, value)

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
        logger.info("Starting Cylc UI Server")
        logger.info(
            f"JupyterHub Service Prefix: {self._jupyter_hub_service_prefix}"
        )
        logger.info(f"Listening on port: {self._port}")
        logger.info(f'Serving UI from: {self.ui_path}')
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
            self.workflows_mgr.update,
            self.scan_interval * 1000
        ).start()
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
    parser.add_argument('--ui-build-dir', action="store")
    parser.add_argument('--debug', action="store_true", dest="debug",
                        default=False)
    args = parser.parse_known_args()[0]

    jupyterhub_service_prefix = os.environ.get(
        'JUPYTERHUB_SERVICE_PREFIX', '/')

    ui_server = CylcUIServer(
        port=args.port,
        ui_build_dir=args.ui_build_dir,
        jupyterhub_service_prefix=jupyterhub_service_prefix
    )

    ui_server.start(args.debug)


__all__ = [
    'MyApplication',
    'CylcUIServer',
    'main'
]
