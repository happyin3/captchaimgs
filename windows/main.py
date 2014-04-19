__author__ = "happyin3"
#coding: utf-8

import pymongo

from thesis import ThesisHandler


def main_thesis(db):
    thesis = ThesisHandler(db)
    thesis.main()


if __name__ == "__main__":
    conn = pymongo.Connection("127.0.0.1", 27017)
    db = conn["captchaimg"]    
    main_thesis(db) 
