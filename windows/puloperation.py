__author__ = "happyin3"
#coding: utf-8

import pysolr


#获取远程数据
class GetRemote(object):
    def __init__(self, remote_url):
        self.solr = pysolr.Solr(remote_url, timeout=10)

    def get_data(self, start, rows=100):
        #连接超时
        list_data = []
        try:
            results = self.solr.search("*:*", start=start, rows=rows, sort="update_time asc")
            for result in results:
                list_data.append(result["path"])
        except:
            pass
        finally:
            return list_data


#新建目录
class MakeDirs(object):
    def __init__(self):
        pass

    def make_dir(self, path):
        #引入模块
        import os
         
        #去除首尾空格
        path = path.strip()
        #去除尾部/符号
        path = path.rstrip("/")
      
        #判断路径是否存在
        exist = os.path.exists(path)
        if not exist:
            os.makedirs(path)
            return True
        else:
            return False

    def main(self):
        result = self.make_dir("../static/images/testimg/")
        if result:
            print "Nice"


if __name__ == "__main__":
    make_dirs = MakeDirs()
    make_dirs.main() 
