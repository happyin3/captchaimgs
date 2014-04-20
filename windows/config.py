__author__ = "happyin3"
#coding: utf-8

import pymongo
import time


def config_thesis(db):
    kind = "thesis"
    remote_url = "http://localhost:8983/solr/papers"
    down_url = "http://202.195.136.17"
    server_address = ["172.16.111.230", 8889]
    convert_url = "http://172.16.111.230:8080/convertserver"

    #配置
    db.configini.insert({"kind": kind, "remoteurl": remote_url, "downurl": down_url, "serverurl": server_address, "converturl": convert_url, "onflag": 1, "time": time.ctime()})
    
    return 

def config_code(db):
    kind = "code"
    down_url = "http://www.drugfuture.com/cnpat/verify.aspx"
    
    #配置
    db.configini.insert({"kind": kind, "downurl": down_url, "onflag": 1, "time": time.ctime()})

    return 

def config_patent(db):
    kind = "patent"
    remote_url = "http://localhost:8983/solr/patent"
    down_url = "http://www.drugfuture.com/cnpat/cn_patent.asp"

    #配置
    db.configini.insert({"kind": kind, "down_url": down_url, "onflag": 1, "time": time.ctime()})

    return


if __name__ == "__main__": 
    conn = pymongo.Connection("127.0.0.1", 27017) 
    db = conn["captchaimg"]
    #config_thesis(db)
    #config_code(db)
    config_patent(db)
