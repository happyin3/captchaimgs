__author__ = "happyin3"
#coding: utf-8

import time

from puloperation import GetRemote


class ThesisHandler(object):
    def __init__(self, db):
        self.db = db

    #远程获取论文url
    def get_remote(self):
        #读取数据集configini，获取远程索引url
        results = self.db.configini.find_one({"kind": "thesis", "onflag": 1}, {"_id": 0, "remoteurl": 1})
        #没有数据
        if results:
            remote_url = results["remoteurl"] 
            #统计数据集urlno的数据，计算start
            count = self.db.urlno.count({"kind": "thesis"})
            get_remote = GetRemote(remote_url)
            list_data = get_remote.get_data(count)
            #正确获取数据
            if len(list_data):
                for data in list_data:
                    #查重
                    exist = self.db.urlno.find_one({"indexflag": data}) 
                    if not exist:
                        #插入数据
                        try:
                            self.db.urlno.insert({"indexflag": url, "kind": "thesis", "convertflag": 0, "extractflag": 0, "downflag": 0, "time": time.ctime()})
                        except:
                            pass
        return

    #格式转换
    def convert(self):
        #读取数据集urlno，获取需转换文件列表
        results = self.db.urlno.find({"kind": "thesis", "convertflag": 0, "downflag": 0}, {"_id": 0, "indexflag": 1})
        #存在文件需要转换
        if results:
            #读取数据集configini，获取配置文件
            config_results = self.db.configini.find_one({"kind": "thesis", "onflag": 1}, {"_id": 0, "downurl": 1, "serverurl": 1, "converturl": 1})
            down_url = config_results["downurl"]
            server_address = config_results["serverurl"]
            convert_url = config_results["converturl"]
            convert_client = ConvertClinet() 
            for urls in results:
                url = urls["indexflag"]
                #下载
