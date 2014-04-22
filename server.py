__author__ = "happyin3"

import tornado.ioloop
import tornado.httpserver
import sys

from application import Application


PORT = "8888"

if __name__ == "__main__":
    if len(sys.argv) > 1:
        PORT = sys.argv[1]
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(PORT)

    print "Development server is running at http://127.0.0.1:%s" %PORT
    print "Quit the server with CONTROL-C"
    #tornado.ioloop.PeriodicCallback(get_patentno.send_post(), 5000).start()
    tornado.ioloop.IOLoop.instance().start()
