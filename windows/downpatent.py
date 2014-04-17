__author__ = "happyin3"
#coding: utf-8


class DownPatent(object):
    def __init__(self, db):
        self.db = db

    #查询专利
    def query_patent(self):
        #读取数据集urlno，获取专利号indexflag
        results = self.db.urlno.find({"kind": "patent", "downflag": 0}, {"_id": 0, "indexflag": 1})
        if results:
            for each_result in results:
                patentno = each_result["indexflag"]
                
                #开始查询
     
