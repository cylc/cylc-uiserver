import argparse
import json
import logging
import os
import signal

from jupyterhub import __version__ as jupyterhub_version
from jupyterhub.services.auth import HubOAuthenticated, HubOAuthCallbackHandler
from jupyterhub.utils import url_path_join
from tornado import web, ioloop
from handlers import *


class MainHandler(HubOAuthenticated, web.RequestHandler):

    # hub_users = ["kinow"]
    # hub_groups = []
    # allow_admin = True

    def initialize(self, path):
        self._static = path

    @web.authenticated
    def get(self):
        """Render the UI prototype."""
        self.set_header("X-JupyterHub-Version", jupyterhub_version)
        index = os.path.join(self._static, "index.html")
        self.write(open(index).read())


class UserProfileHandler(HubOAuthenticated, web.RequestHandler):

    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        self.set_header("Content-Type", 'application/json')

    @web.authenticated
    def get(self):
        self.write(json.dumps(self.get_current_user()))


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
            self._static = os.path.join(script_dir, static)
        self._jupyter_hub_service_prefix = jupyter_hub_service_prefix

    def _make_app(self):
        """Crete a Tornado web application."""
        logging.info(self._static)
        return MyApplication(
            static_path=self._static,
            debug=True,
            handlers=[
                (rf"{self._jupyter_hub_service_prefix}(.*.(css|js))", web.StaticFileHandler, {"path": self._static}),
                (rf"{self._jupyter_hub_service_prefix}((fonts|img)/.*)", web.StaticFileHandler, {"path": self._static}),
                (rf"{self._jupyter_hub_service_prefix}(favicon.png)", web.StaticFileHandler, {"path": self._static}),

                (r"/(.*.(css|js))", web.StaticFileHandler, {"path": self._static}),
                (r"/((fonts|img)/.*)", web.StaticFileHandler, {"path": self._static}),
                (r"/(favicon.png)", web.StaticFileHandler, {"path": self._static}),

                (url_path_join(self._jupyter_hub_service_prefix, 'oauth_callback'), HubOAuthCallbackHandler),
                (url_path_join(self._jupyter_hub_service_prefix, 'userprofile'), UserProfileHandler),
                (url_path_join(self._jupyter_hub_service_prefix, 'suites'), CylcScanHandler),

                (self._jupyter_hub_service_prefix, MainHandler, {"path": self._static}),
            ],
            # FIXME: decide (and document) whether cookies will be permanent after server restart.
            cookie_secret="cylc-secret-cookie"
        )

    def start(self):
        app = self._make_app()
        signal.signal(signal.SIGINT, app.signal_handler)
        app.listen(self._port)
        ioloop.PeriodicCallback(app.try_exit, 100).start()
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
    parser.add_argument('-s', '--static', action="store", dest="static", required=True)
    args = parser.parse_args()

    jupyterhub_service_prefix = os.environ.get('JUPYTERHUB_SERVICE_PREFIX', '/')
    logging.info(f"JupyterHub Service Prefix: {jupyterhub_service_prefix}")
    ui_server = CylcUIServer(port=args.port, static=args.static, jupyter_hub_service_prefix=jupyterhub_service_prefix)
    logging.info(f"Listening on {args.port} and serving static content from {args.static}")

    logging.info("Starting Cylc UI")
    ui_server.start()


if __name__ == "__main__":
    main()
