__author__ = "happyin3"
#coding: utf-8


import tornado.web


class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        return self.get_secure_cookie("username")


class MainHandler(BaseHandler):
    def get(self):
        if not self.current_user:
            self.render("index.html")
            return
        self.render("index.html")


class PatentHandler(tornado.web.RequestHandler):
    def post(self):
        patentno = self.get_argument("patentno")
        if not patentno:
            self.write("1")  #input error
        else:
            #数据集中时候存在所需专利号
            exist_result = self.application.db.urlno.find_one({"indexflag": patentno})
            if not exist_result:
                #不存在url
                self.write("2") 
            else:
                #是否已下载
                exist_result = self.application.db.urlno.find_one({"indexflag": patentno, "downflag": 1})
                if exist_result:
                    #没有下载成功
                    self.write("3")
                else:
                    #是否已提取图片
                    exist_result = self.application.db.urlno.find_one({"indexflag": patentno, "extractflag": 1})
                    if not exist_result:
                        #没有提取图片 
                        self.write("4")
                    else:
                        #是否存在图片
                        exist_result = self.application.db.find_one({"indexflag": patentno}, {"_id": 0, "mergepath": 1})
                        if not len(exist_result["mergepath"]):
                            #不存在图片
                            self.write("5")
                        else:
                            complete_merge_path = "http://signals.hyit.edu.cn:8888/" + exist_result["mergepath"]
                            self.write(complete_merge_path)
        return 

class ThesisHandler(tornado.web.RequestHandler):
    def post(self):
        url = self.get_argument("url")
        if not url:
            self.write("1")  #input error
        else:
            #数据库中是否存在所需url
            exist_result = self.application.db.urlno.find_one({"indexflag": url})
            if not exist_result:
                #不存在url
                self.write("2")
            else:
                #是否下载成功
                exist_result = self.application.db.urlno.find_one({"indexflag": url, "downflag": 2})
                if exist_result:
                    #下载失败
                    self.write("3")
                else:
                    #是否已完成格式转换
                    exist_result = self.application.db.urlno.find_one({"indexflag": url, "convertflag": 1})
                    if not exist_result:
                        #没有格式转换
                        self.write("4")
                    else:
                        #是否已完成图片提取
                        exist_result = self.application.db.urlno.find_one({"indexflag": url, "extractflag": 1})
                        if not exist_result:
                            #没有提取图片
                            self.write("5")
                        else:
                            #是否存在图片
                            extract_result = self.application.db.mergeimg.find_one({"indexflag": url}, {"_id": 0, "mergepath": 1})
                            merge_path = extract_result["mergepath"]
                            if not len(merge_path):
                                #不存在图片
                                self.write("6")
                            else:
                                complete_merge_path = "http://signals.hyit.edu.cn:8888/" + merge_path
                                self.write(complete_merge_path)
        return
