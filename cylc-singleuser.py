import tornado.ioloop
import tornado.web
import sys
import os
import signal
import logging


class MainHandler(tornado.web.RequestHandler):

    def get(self, username):
        # At this point we would have Cylc running, so we just ned to have
        # a handler that gives the user's Dashboard... this acts now as
        # the entry point, in the same way that the GUI gcylc was before...
        self.write(f"""
        <p>Hello, world {username} !</p>
        <p>Click <a href="/hub/home">here</a> to go back to the hub... it is because
        I am templeteless for now (a good joke, c'mon!)</p>
        <p>I am process ID {os.getpid()}</p>       
        """)


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
    return MyApplication([
        (r"/user/(.*)", MainHandler),
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
