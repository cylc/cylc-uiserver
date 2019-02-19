import logging
import os
import signal
import sys

import tornado.ioloop
import tornado.web


class MainHandlerOld(tornado.web.RequestHandler):
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


class MainHandler(tornado.web.RequestHandler):

    def get(self):
        """Render the UI prototype."""
        index = os.path.join(os.path.dirname(__file__), "static", "index.html")
        self.write(open(index).read())


class MyApplication(tornado.web.Application):
    is_closing = False

    def signal_handler(self, signum, frame):
        logging.info('exiting...')
        self.is_closing = True

    def try_exit(self):
        if self.is_closing:
            # clean up here
            tornado.ioloop.IOLoop.instance().stop()
            logging.info('exit success')


def make_app():
    static_path = os.path.join(os.path.dirname(__file__), "static")
    return MyApplication(
        static_path=static_path,
        debug=True,
        handlers=[
            # (r"/user/(.*)", MainHandler),
            (r"/(css/.*)", tornado.web.StaticFileHandler, {"path": static_path}),
            (r"/(fonts/.*)", tornado.web.StaticFileHandler, {"path": static_path}),
            (r"/(img/.*)", tornado.web.StaticFileHandler, {"path": static_path}),
            (r"/(js/.*)", tornado.web.StaticFileHandler, {"path": static_path}),
            (r"/(favicon.png)", tornado.web.StaticFileHandler, {"path": static_path}),

            (r"/user/.*/(css/.*)", tornado.web.StaticFileHandler, {"path": static_path}),
            (r"/user/.*/(fonts/.*)", tornado.web.StaticFileHandler, {"path": static_path}),
            (r"/user/.*/(img/.*)", tornado.web.StaticFileHandler, {"path": static_path}),
            (r"/user/.*/(js/.*)", tornado.web.StaticFileHandler, {"path": static_path}),
            (r"/user/.*/(favicon.png)", tornado.web.StaticFileHandler, {"path": static_path}),

            (r"/.*", MainHandler),
        ])


if __name__ == "__main__":
    app = make_app()
    signal.signal(signal.SIGINT, app.signal_handler)
    if len(sys.argv) > 1:
        app.listen(int(sys.argv[1]))
    else:
        app.listen(8888)
    tornado.ioloop.PeriodicCallback(app.try_exit, 100).start()
    try:
        tornado.ioloop.IOLoop.current().start()
    except KeyboardInterrupt:
        tornado.ioloop.IOLoop.instance().stop()
