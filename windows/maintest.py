__author__ = "happyin3"
#coding: utf-8

import pymongo
import time
from PIL import Image

from getremote import GetUrl
from getremote import GetPatentNO
from convertclient import ConvertClient
from extractimg import ExtractImage
from downcode import DownCode
from dealcode import DealImage
from neuralwork import NeuralWork


class ImageHandler(object):
    def __init__(self):
        conn = pymongo.Connection("127.0.0.1", 27017)
        self.db = conn["captchaimg"]
    
    #远程获取url
    def get_url(self):
        geturl = GetUrl()
        #读取数据集urlno，统计urlno中所有文档数
        count = self.db.urlno.count()
        list_url = geturl.get_url(count)
        
        #写入数据集urlno，存入url、文档类型、图片格式转换标志、提取图片标志、时间
        for url in list_url:
            #查重
            exist_result = self.db.urlno.find_one({"indexflag": url})
            if not exist_result:
                self.db.urlno.insert({"indexflag": url, "kind": "thesis", "convertflag": 0, "extractflag": 0, "downflag": 0, "time": time.ctime()})
        
        return

    #远程获取专利号
    def get_patentno(self):
        getpatentno = GetPatentNO()
        list_patentno = getpatentno.get_patentno()

        #写入数据集urlno，存入patentno、文档类型、图片格式转换标志、提取图片标志、时间
        for url in list_patentno:
            #查重
            exit_result = self.db.urlno.find_one({"indexflag": url})
            if not exit_result:
                self.db.urlno.insert({"indexflag": url, "kind": "patent", "convertflag": 1, "extractflag": 0, "downflag": 0, "time": time.ctime()})

        return
  
    #转换图片
    def convert_image(self):
        #读取数据集urlno中图片格式转换标志为0的url，并返回indexflag
        list_pdf_url = self.db.urlno.find({"kind": "thesis", "convertflag": 0, "downflag": 0}, {"indexflag": 1})

        #下载PDF，并转成图片
        convert_client = ConvertClient()
        for pdf_urls in list_pdf_url:
            pdf_url = pdf_urls["indexflag"]
            list_save_name = convert_client.connect_server(pdf_url)
            #PDF下载失败
            if len(list_save_name):
                #存入数据库，存入 URL、图片路径、时间
                #设置URL下载标记为 1，已下载，图片处理标记为0，为提取图片
                exist_result = self.db.convertimg.find_one({"indexflag": pdf_url})
                if not exist_result:
                    self.db.convertimg.insert({"indexflag": pdf_url, "convertpath": list_save_name, "time": time.ctime()})
                self.db.urlno.update({"indexflag": pdf_url}, {"$set": {"convertflag": 1, "downflag": 1}})
            else:
                #存储数据
                self.db.urlno.update({"indexflag": pdf_url}, {"$set": {"downflag": 2}})

        return
    
    #提取图片
    def extract_image(self):
        #读取数据集pdfurl中图片提取标志为0的url，并返回url
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
            exist_result = self.db.dealimg.find_one({"indexflag": url})
            if not exist_result:
                self.db.dealimg.insert({"indexflag": url, "dealpath": list_deal_image_path, "time": time.ctime()})
            exist_result = self.db.extractimg.find_one({"indexflag": url})
            if not exist_result:
                self.db.extractimg.insert({"indexflag": url, "extractpath": list_extract_image_path, "time": time.ctime()})
            exist_result = self.db.mergeimg.find_one({"indexflag": url})
            if not exist_result:
                self.db.mergeimg.insert({"indexflag": url, "mergepath": final_merge_image_path, "time": time.ctime()})

            self.db.urlno.update({"indexflag": url}, {"$set": {"extractflag": 1}})
            
            i = i + 1
            print i
            if i > 9:
                break
        return

    def main(self):
        print "geturl"
        #self.get_url()
        print "convert_image"
        #self.convert_image()
        print "extract_image"
        self.extract_image()


class CodeHandler(object):
    def __init__(self): 
        conn = pymongo.Connection("127.0.0.1", 27017) 
        self.db = conn["captchaimg"]

    #下载验证码
    def down_code(self):
        url = "http://www.drugfuture.com/cnpat/verify.aspx"
        number = 50
        down = DownCode()
        list_save_path = down.main(url, number)
        
        #存入数据库downcode，验证码路径
        for save_path in list_save_path:
            exist_result = self.db.downcode.find_one({"codepath": save_path})
            if not exist_result:
                self.db.downcode.insert({"codepath": save_path, "dealflag": 0, "splitflag": 0, "time": time.ctime()}) 
    
    #更新验证码明码
    def update_plain(self):
        trans_rules = "0123456789abcedf"
        plain_text = []
        pathtxt = open("plaincode.txt", "r")
        while True:
            line = pathtxt.readline()
            line = line.strip("\n")
            if not line:
                break
            else:
                plain_text.append(line)
        pathtxt.close() 
        
        all_plain_text = []
        for text in plain_text:
            split_text = text.split(".")
            each_plain_text = []
            for each_text in split_text:
                index = trans_rules.find(each_text)
                each_plain_text.append(index)
            all_plain_text.append(each_plain_text)
        
        #读取数据库downcode，获取所有验证码路径
        all_down_code = self.db.downcode.find({}, {"_id": 0, "codepath": 1})
        
        if all_down_code: 
            for code_path, each_text in zip(all_down_code, all_plain_text): 
                code_path_temp = code_path["codepath"]
                #更新数据库downcode，更新验证码明文
                self.db.downcode.update({"codepath": code_path_temp}, {"$set": {"text": each_text}}) 

    def deal_code(self):
        #读取数据库downcode，获取验证码路径
        deal_image = DealImage()
        all_down_code = self.db.downcode.find({"dealflag": 0}, {"_id": 0, "codepath": 1})
        if all_down_code:
            for code_path in all_down_code:
                code_path_temp = code_path["codepath"]
                #预处理图片
                code_path_temps = "../%s" % code_path_temp
                save_path = deal_image.main_deal_image(code_path_temps)
                if len(save_path):
                    #存入数据库dealcode，验证码路径和验证码处理后路径
                    exist_result = self.db.dealcode.find_one({"codepath": code_path_temp})
                    if not exist_result:
                        self.db.dealcode.insert({"codepath": code_path_temp, "dealpath": save_path, "time": time.ctime()})
                        self.db.downcode.update({"codepath": code_path_temp}, {"$set": {"dealflag": 1}})
                    
                time.sleep(1)

    def split_code(self):
        #读取数据集dealcode，获取处理验证码图片路径
        deal_image = DealImage()
        all_code_path = self.db.downcode.find({"dealflag": 1, "splitflag": 0}, {"_id": 0, "codepath": 1})
        if all_code_path:
            all_deal_path = []
            all_code_paths = []
            for each_code in all_code_path:
                each_code_path = each_code["codepath"]
                all_code_paths.append(each_code_path)
                #读取数据集dealcode，获取处理图片路径
                each_deal_path = self.db.dealcode.find_one({"codepath": each_code_path}, {"_id": 0, "dealpath": 1})
                if each_deal_path:
                    all_deal_path.append(each_deal_path["dealpath"])
            
            for each_deal_path, each_code_path in zip(all_deal_path, all_code_paths):
                each_deal_path_temp = "../%s" % each_deal_path
                list_split_image_path = deal_image.main_split_image(each_deal_path_temp)
                if len(list_split_image_path):
                    #存入数据集splitcode，验证码路径和分割图片路径
                    exist_result = self.db.splitcode.find_one({"codepath": each_code_path})
                    if not exist_result:
                        self.db.splitcode.insert({"codepath": each_code_path, "splitpath": list_split_image_path, "time": time.ctime()})
                        #更新数据集downcode，分割标志为1
                        self.db.downcode.update({"codepath": each_code_path}, {"$set": {"splitflag": 1}})
                    else:
                        self.db.downcode.update({"codepath": each_code_path}, {"$set": {"splitflag": 0}})
                 
    #训练神经网络
    def train_net(self):
        #读取数据集splitcode，获取分割图片路径
        all_split_path = self.db.splitcode.find({}, {"_id": 0})
        if all_split_path:
            list_code_path = []
            list_split_path = []
            for each_code in all_split_path:
                list_code_path.append(each_code["codepath"])
                for each_split_path in each_code["splitpath"]:
                    list_split_path.append(each_split_path)

            #读取数据集downcode，获取验证码明码text
            list_text_num = []
            for each_code in list_code_path:
                results = self.db.downcode.find_one({"codepath": each_code}, {"_id": 0, "text": 1})
                if results:
                    for each in results["text"]:
                        each = each * 1.0 / 100
                        each_text = []
                        each_text.append(each)
                        list_text_num.append(each_text)
            
            #生成输入数据
            list_train_input_data = []
            for each_code in list_split_path:
                each_code_temp = "../%s" % each_code
                image = Image.open(each_code_temp)
                each_train_input_data = []
                for x in xrange(image.size[1]):
                    for y in xrange(image.size[0]):
                        if image.getpixel((y, x)):
                            each_train_input_data.append(0)
                        else:
                            each_train_input_data.append(1)
                list_train_input_data.append(each_train_input_data)

            #生成目标数据
            list_train_output_data = list_text_num
            
            for each in list_train_input_data:
                print len(each)
            #开始训练
            net_size = [10, 1]
            neural = NeuralWork()
            net = neural.train_net(list_train_input_data, list_train_output_data, net_size)   

    def main(self):
        print "downcode"
        #self.down_code()
        print "updateplain"
        #self.update_plain()
        print "dealcode"
        #self.deal_code()
        print "splitcode"
        #self.split_code()
        print "trainnet"
        self.train_net() 

if __name__ == "__main__":
    #image_handler = ImageHandler()
    #image_handler.main()

    code_handler = CodeHandler()
    code_handler.main()
           
