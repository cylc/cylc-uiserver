#!/usr/bin/env python3

# -*- coding: utf-8 -*-
# Copyright (C) 2019 NIWA & British Crown (Met Office) & Contributors.
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
import logging
import os
import signal

from cylc.flow.network.schema import schema
from jupyterhub.services.auth import HubOAuthCallbackHandler
from jupyterhub.utils import url_path_join
from tornado import web, ioloop

from handlers import *
from workflows_mgr import WorkflowsManager
from data_mgr import DataManager
from resolvers import Resolvers


class MyApplication(web.Application):
    is_closing = False

    def signal_handler(self, signum, frame):
        logging.info('exiting...')
        self.is_closing = True

    def try_exit(self):
        if self.is_closing:
            # clean up here
            ioloop.IOLoop.instance().stop()
            logging.info('exit success')


class CylcUIServer(object):

    def __init__(self, port, static, jupyter_hub_service_prefix):
        self._port = port
        if os.path.isabs(static):
            self._static = static
        else:
            script_dir = os.path.dirname(__file__)
            self._static = os.path.abspath(os.path.join(script_dir, static))
        self._jupyter_hub_service_prefix = jupyter_hub_service_prefix
        self.ws_mgr = WorkflowsManager()
        self.data_mgr = DataManager(self.ws_mgr)
        self.resolvers = Resolvers(
            self.ws_mgr, self.data_mgr)

    def _make_app(self):
        """Crete a Tornado web application."""
        logging.info(self._static)
        return MyApplication(
            static_path=self._static,
            debug=True,
            handlers=[
                (rf"{self._jupyter_hub_service_prefix}(.*.(css|js))",
                 web.StaticFileHandler, {"path": self._static}),
                (rf"{self._jupyter_hub_service_prefix}((fonts|img)/.*)",
                 web.StaticFileHandler, {"path": self._static}),
                (rf"{self._jupyter_hub_service_prefix}(favicon.png)",
                 web.StaticFileHandler, {"path": self._static}),

                (r"/(.*.(css|js))",
                 web.StaticFileHandler, {"path": self._static}),
                (r"/((fonts|img)/.*)",
                 web.StaticFileHandler, {"path": self._static}),
                (r"/(favicon.png)",
                 web.StaticFileHandler, {"path": self._static}),

                (url_path_join(
                    self._jupyter_hub_service_prefix, 'oauth_callback'),
                    HubOAuthCallbackHandler),
                (url_path_join(
                    self._jupyter_hub_service_prefix, 'userprofile'),
                    UserProfileHandler),
                (url_path_join(
                    self._jupyter_hub_service_prefix, 'routes'),
                    RoutesHandler),
                (url_path_join(
                    self._jupyter_hub_service_prefix, 'suites'),
                    CylcScanHandler),

                (rf"{self._jupyter_hub_service_prefix}?",
                    MainHandler, {"path": self._static}),

                # graphql
                (url_path_join(self._jupyter_hub_service_prefix,
                               '/graphql'),
                    UIServerGraphQLHandler,
                    dict(schema=schema, resolvers=self.resolvers)),
                (url_path_join(self._jupyter_hub_service_prefix,
                               '/graphql/batch'),
                    UIServerGraphQLHandler,
                    dict(schema=schema, resolvers=self.resolvers, batch=True)),
                (url_path_join(self._jupyter_hub_service_prefix,
                               '/graphql/graphiql'),
                    UIServerGraphQLHandler,
                    dict(schema=schema, resolvers=self.resolvers,
                         graphiql=True)),
            ],
            # FIXME: decide (and document) whether cookies will be permanent
            # after server restart.
            cookie_secret="cylc-secret-cookie"
        )

    def start(self):
        app = self._make_app()
        signal.signal(signal.SIGINT, app.signal_handler)
        app.listen(self._port)
        ioloop.PeriodicCallback(app.try_exit, 100).start()
        # Discover workflows on initial start up.
        ioloop.IOLoop.current().add_callback(self.ws_mgr.gather_workflows)
        # If the client is already established it's not overridden,
        # so the following callbacks can happen at the same time.
        ioloop.PeriodicCallback(self.ws_mgr.gather_workflows, 10000).start()
        ioloop.PeriodicCallback(
            self.data_mgr.entire_workflow_update, 5000).start()
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
    args = parser.parse_known_args()[0]

    jupyterhub_service_prefix = os.environ.get(
        'JUPYTERHUB_SERVICE_PREFIX', '/')
    logging.info(f"JupyterHub Service Prefix: {jupyterhub_service_prefix}")
    ui_server = CylcUIServer(
        port=args.port,
        static=args.static,
        jupyter_hub_service_prefix=jupyterhub_service_prefix
    )
    logging.info(f"Listening on {args.port} and serving static content from "
                 f"{args.static}")

    logging.info("Starting Cylc UI")
    ui_server.start()


if __name__ == "__main__":
    main()


__all__ = ['MainHandler', 'UserProfileHandler', 'MyApplication',
           'CylcUIServer', 'main']
