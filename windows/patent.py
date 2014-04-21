__author__ = "happyin3"
#coding: utf-8

import time

from puloperation import GetRemote
from patentclass import DownPatent


#专利
class PatentHandler(object):
    def __init__(self, db):
        self.db = db

    #远程获取专利号
    def get_remote(self):
        #读取数据集configini，获取远程索引url
        results = self.db.configini.find_one({"kind": "patent", "onflag": 1}, {"_id": 0, "remoteurl": 1})
        #没有数据
        if results:
            remote_url = results["remoteurl"]
            print remote_url
            #统计数据集urlno的数据，计算start
            count = self.db.urlno.find({"kind": "patent"}).count()
            get_remote = GetRemote(remote_url)
            list_data = get_remote.get_data("patent", count)
            #正确获取数据
            if len(list_data):
                for data in list_data:
                    #查重
                    exist = self.db.urlno.find_one({"indexflag": data})
                    if not exist:
                        #插入数据
                        try:
                            self.db.urlno.insert({"indexflag": data, "kind": "patent", "downflag": 0, "extractflag": 0, "time": time.ctime()})
                        except: pass
        return

    #下载专利图片
    def download(self):
        #读取数据集urlno，获取专利号
        results = self.db.urlno.find({"kind": "patent", "downflag": 0}, {"_id": 0, "indexflag": 1})
        if results:
            #读取数据集configini，获取专利下载配置文件
            config_results = self.db.configini.find_one({"kind": "patent", "onflag": 1}, {"_id": 0, "downurl": 1})
            down_url = config_results["downurl"]
            down_patent = DownPatent(self.db, down_url)
            #下载
            i = 0
            for result in results:
                patentno = result["indexflag"]
                print patentno
                try:
                    download_link = down_patent.download(patentno)
                    if len(download_link):
                        #下载专利
                        print download_link
                except: pass
                i = i + 1
                if i > 5:
                    break
        return

    #提取图片
    def extract_image(self):
        #读取数据集urlno，获取专利号
        results = self.db.urlno.find({"kind": "patent", "downflag": 1}, {"_id": 0, "indexflag": 1})
        if results:
            pass

    def main(self):
        print "getremote"
        #self.get_remote()
        print "download"
        self.download() 

