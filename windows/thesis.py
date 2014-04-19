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
            count = self.db.urlno.find({"kind": "thesis"}).count()
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
            convert_client = ConvertClient(down_url, server_address, convert_url)
            for urls in results:
                url = urls["indexflag"]
                #下载
                list_save_name = convert_clinet.connect_server(url)
                #PDF下载失败
                if len(list_save_name):
                    #存入数据集convertimg，存入url、图片路径、时间
                    #设置url下载标记为1，已下载，图片处理标记为0，未提取图片
                    exist = self.db.convertimg.find_one({"indexflag": url})
                    if not exist:
                        try:
                            self.db.convertimg.insert({"indexflag": pdf_url, "convertpath": list_save_name, "time": time.ctime()})
                            self.db.urlno.update({"indexflag": pdf_url}, {"$set": {"convertflag": 1, "downflag": 1}})
                        except:
                            pass
                    else:
                        #更新数据集urlno
                        self.db.urlno.update({"indexflag": pdf_url}, {"$set": {"downflag": 2}})
                
                break
        return

    #提取图片
    def extract_image(self):
        #读取数据集urlno中图片提取标志为0的url，并返回url
        list_url = self.db.urlno.find({"convertflag": 1, "extractflag": 0}, {"indexflag": 1})

        i = 0
        for urls in list_url:
            url = urls["indexflag"]
            #读取数据集convertimg中url想对应的转换图片
            list_convert_img = self.db.convertimg.find({"indexflag": url}, {"convertpath": 1})

            for item in list_convert_img:
                list_convert_imgs = item["convertpath"]

            #提取图片
            list_save_path = []
            for convert_img in list_convert_imgs:
                image = Image.open(convert_img)
                image = image.convert("L")
                extract_img = ExtractImage(image)
                list_each_save_path = extract_img.main()
                list_save_path.append(list_each_save_path)

            #分别提取不同路径
            list_deal_image_path = []
            list_extract_image_path = []
            list_merge_image_path = []
            for each_save_path in list_save_path:
                list_deal_image_path.append(each_save_path[0][0])
                if len(each_save_path[0][1]):
                    list_merge_image_path.append(each_save_path[0][1])
                if len(each_save_path[0][2]):
                    for each_extract_image_path in each_save_path[0][2]:
                        list_extract_image_path.append(each_extract_image_path)

            #合并单页图片
            final_merge_image_path = ""
            if len(list_merge_image_path):
                list_merge_image = []
                for each_merge_image_path in list_merge_image_path:
                    image = Image.open(each_merge_image_path)
                    list_merge_image.append(image)
                
                extract_img = ExtractImage()
                final_merge_image_path = extract_img.image_merge(list_merge_image)

            #写入数据集dealimg,extractimg,mergeimg
            exist = self.db.dealimg.find_one({"indexflag": url})
            if not exist:
                try:
                    self.db.dealimg.insert({"indexflag": url, "dealpath": list_deal_image_path, "time": time.ctime()})
                except:
                    pass

            exist = self.db.extractimg.find_one({"indexflag": url})
            if not exist:
                try:
                    self.db.extractimg.insert({"indexflag": url, "extractpath": list_extract_image_path, "time": time.ctime()})
                except:
                    pass

            exist = self.db.mergeimg.find_one({"indexflag": url})
            if not exist:
                try:
                    self.db.mergeimg.insert({"indexflag": url, "mergepath": final_merge_image_path, "time": time.ctime()})
                except:
                    pass
            try:
                self.db.urlno.update({"indexflag": url}, {"$set": {"extractflag": 1}})
            except:
                pass

            i = i + 1
            print i
            if i > 9:
                break
        return
 
    def main(self):
        print "GetRemote"
        self.get_remote()
        print "Convert"
        #self.convert()
        print "ExtractImage"
        #self.extract_image()
