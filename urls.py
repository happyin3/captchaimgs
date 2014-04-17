__author__ = "happyin3"
#coding: utf-8


from handlers.index import MainHandler
from handlers.index import PatentHandler
from handlers.index import ThesisHandler


urls = [
    (r'/', MainHandler),
    (r'/getPatentImage', PatentHandler),
    (r'/getThesisImage', ThesisHandler),
]
