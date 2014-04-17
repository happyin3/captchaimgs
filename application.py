__author = "happyin3"
#coding: utf-8

import os
import tornado.web
import pymongo

from urls import urls


class Application(tornado.web.Application):
    def __init__(self):
        handlers = urls

        SETTINGS = dict(
            template_path = os.path.join(os.path.dirname(__file__), "templates"),
            static_path = os.path.join(os.path.dirname(__file__), "static"),
            debug = True,
        )
        
        conn = pymongo.Connection("localhost", 27017)
        self.db = conn["captchaimg"]

        tornado.web.Application.__init__(self, handlers, 
            cookie_secret="61oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo=",
            **SETTINGS
        )

