import json
import logging
import os
import signal
import sys

from jupyterhub import __version__ as jupyterhub_version
from jupyterhub.services.auth import HubOAuthenticated, HubOAuthCallbackHandler
from jupyterhub.utils import url_path_join
from tornado import web, ioloop


class MainHandlerOld(web.RequestHandler):
    """A handler that displays the user name, and also the PID. Useful
    for troubleshooting"""

    def get(self, username):
        """
        Get for user area.

        At this point we would have Cylc running, so we just ned to have
        a handler that gives the user's Dashboard... this acts now as
        the entry point, in the same way that the GUI gcylc was before...
        """
        self.write(f"""
        <p>Hello, world {username} !</p>
        <p>Click <a href="/hub/home">here</a> to go back to the hub.</p>
        <p>I am process ID {os.getpid()}</p>       
        """)


class MainHandler(HubOAuthenticated, web.RequestHandler):

    # hub_users = ["kinow"]
    # hub_groups = []
    # allow_admin = True

    @web.authenticated
    def get(self):
        """Render the UI prototype."""
        self.set_header("X-JupyterHub-Version", jupyterhub_version)
        index = os.path.join(os.path.dirname(__file__), "static", "index.html")
        self.write(open(index).read())


class UserProfileHandler(HubOAuthenticated, web.RequestHandler):

    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.setl_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
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

    @staticmethod
    def _make_app():
        """Crete a Tornado web application."""
        static_path = os.path.join(os.path.dirname(__file__), "static")
        return MyApplication(
            static_path=static_path,
            debug=True,
            handlers=[
                (r"/(css/.*)", web.StaticFileHandler, {"path": static_path}),
                (r"/(fonts/.*)", web.StaticFileHandler, {"path": static_path}),
                (r"/(img/.*)", web.StaticFileHandler, {"path": static_path}),
                (r"/(js/.*)", web.StaticFileHandler, {"path": static_path}),
                (r"/(favicon.png)", web.StaticFileHandler, {"path": static_path}),

                (r"/user/.*/(css/.*)", web.StaticFileHandler, {"path": static_path}),
                (r"/user/.*/(fonts/.*)", web.StaticFileHandler, {"path": static_path}),
                (r"/user/.*/(img/.*)", web.StaticFileHandler, {"path": static_path}),
                (r"/user/.*/(js/.*)", web.StaticFileHandler, {"path": static_path}),
                (r"/user/.*/(favicon.png)", web.StaticFileHandler, {"path": static_path}),

                (url_path_join(os.environ['JUPYTERHUB_SERVICE_PREFIX'], 'oauth_callback'), HubOAuthCallbackHandler),
                (url_path_join(os.environ['JUPYTERHUB_SERVICE_PREFIX'], 'userprofile'), UserProfileHandler),

                (os.environ['JUPYTERHUB_SERVICE_PREFIX'], MainHandler),
            ],
            cookie_secret="cylc123"
        )

    def start(self, *args):
        app = self._make_app()
        signal.signal(signal.SIGINT, app.signal_handler)
        app.listen(int(args[0]))
        ioloop.PeriodicCallback(app.try_exit, 100).start()
        try:
            ioloop.IOLoop.current().start()
        except KeyboardInterrupt:
            ioloop.IOLoop.instance().stop()


if __name__ == "__main__":
    port = 8888
    if len(sys.argv) > 1:
        port = int(sys.argv[1])
    ui_server = CylcUIServer()
    ui_server.start(port)
