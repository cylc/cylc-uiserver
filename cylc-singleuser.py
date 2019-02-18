import tornado.ioloop
import tornado.web
import sys


class MainHandler(tornado.web.RequestHandler):

    def get(self, username):
        # At this point we would have Cylc running, so we just ned to have
        # a handler that gives the user's Dashboard... this acts now as
        # the entry point, in the same way that the GUI gcylc was before...
        self.write("Hello, world " + username + "!")


def make_app():
    return tornado.web.Application([
        (r"/user/(.*)", MainHandler),
    ])


if __name__ == "__main__":
    app = make_app()
    if len(sys.argv) > 1:
        app.listen(int(sys.argv[1]))
    else:
        app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
