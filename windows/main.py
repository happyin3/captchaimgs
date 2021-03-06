__author__ = "happyin3"
#coding: utf-8

import pymongo

from thesis import ThesisHandler
from codeclass import CodeClass
from patent import PatentHandler


def main_thesis(db):
    thesis = ThesisHandler(db)
    thesis.main()


def main_code(db):
    code = CodeClass(db)
    code.main()

def main_patent(db):
    patent = PatentHandler(db)
    patent.main()

if __name__ == "__main__":
    conn = pymongo.Connection("127.0.0.1", 27017)
    db = conn["captchaimg"]    
    main_thesis(db) 
    #main_code(db)
    #main_patent(db)
