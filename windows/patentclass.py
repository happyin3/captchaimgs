__author__ = "happyin3"
#coding: utf-8

import time
import pymongo
from PIL import Image
from splinter import Browser

from codeclass import CodeHandler
from codeclass import NeuralWork


#下载专利
class DownPatent(object):
    def __init__(self, db, down_url):
        self.db = db
        self.down_url = down_url
        #self.browser = Browser("phantomjs", wait_time=20)
        self.browser = Browser()

    #下载专利
    def download(self, patentno):
        #访问网页
        #网页加载超时
        #down_flag, 0：未下载，1：不存在，2：下载失败
        download_link = ""
        down_flag = 0
        if True:
            self.browser.visit(self.down_url)
            if not self.browser.is_element_not_present_by_value("查询", wait_time=10):
                #填写专利号
                self.browser.fill("cnpatentno", patentno)
                self.browser.find_by_value("查询").first.click()

                #连接超时，404
                if self.browser:
                    #一个最多循环20次
                    code_handler = CodeHandler()
                    #填写验证码
                    list_fill_text = []
                    #验证码路径
                    list_code_path = []
                    #验证码分割标志
                    list_split_flag = []
                    #验证码识别标志
                    list_reg_flag = []
                    for code_num in xrange(20):
                        #查找验证码
                        if not self.browser.is_element_not_present_by_id("getcode", wait_time=5):
                            #截图
                            self.browser.driver.maximize_window()
                            self.browser.driver.save_screenshot("screenshot.png")
                            #获取验证码图片
                            image = Image.open("screenshot.png")
                            image_code = image.crop((3,50, 55, 71))
                            save_path = "static/images/onlinecode/" + time.ctime() + ".png"
                            save_path_temp = "../%s" % save_path
                            image_code.save(save_path_temp)
                            list_code_path.append(save_path)

                            #分割图片
                            list_split_image = self.deal_split(code_handler, image_code)
                            
                            #识别，如果能正确识别，则识别，不能，则重新获取验证码      
                            if len(list_split_image) == 4:
                                list_split_flag.append(1)
                                reg_plain_text = self.reg_code(list_split_image)
                                fill_text = "".join(reg_plain_text)
                                print fill_text         
                                list_fill_text.append(fill_text)
                                #填写验证码
                                hand_fill_text = raw_input("Enter fill text:")
                                self.browser.fill("ValidCode", hand_fill_text)
                                self.browser.find_by_value("确定").first.click()

                                #判断识别结果 
                                if not self.browser.is_text_present("验证码输入错误，请返回重新输入。", wait_time=5):
                                    if not self.browser.is_text_present("没有找到该专利!请检查输入的专利号或公开号是否正确!", wait_time=5):
                                        down_link_one = self.browser.find_link_by_text("申请公开说明书图形下载(标准版)")
                                        down_link_two = self.browser.find_link_by_text("申请公开说明书图形下载(极速版)")
                                        if down_link_one or down_link_two:
                                            list_reg_flag.append(1)
                                            if down_link_one:
                                                self.browser.click_link_by_text("申请公开说明书图形下载(标准版)")
                                            else:
                                                self.browser.click_link_by_text("申请公开说明书图形下载(极速版)")
                          
                                            #查找下载链接
                                            download_a = self.browser.find_link_by_text("下载专利")
                                            if download_a:
                                                download_link = download_a["href"]
                                            
                                                #找到下载链接
                                                down_flag = 3
                                                break
                                            else:
                                                #下载失败
                                                down_flag = 2
                                                break
                                        else:
                                            list_reg_flag.append(0)
                                            self.browser.back()
                                            self.browser.reload()
                                    else:
                                        list_reg_flag.append(1)
                                        #没有专利
                                        down_flag = 1
                                        break
                                else:
                                    list_reg_flag.append(0)
                                    self.browser.back()
                                    self.browser.reload()
                            else:
                                list_split_flag.append(0)
                                self.browser.reload()
                    
                    #存入数据集onlinecode，专利号，验证码路径，识别码，识别标志，不可分标志，时间
                    
                    for code_path, fill_text, split_flag, reg_flag in zip(list_code_path,list_fill_text, list_split_flag, list_reg_flag):
                        try:
                            self.db.onlinecode.insert({"indexflag": patentno, "codepath": code_path, "filltext": fill_text, \
                                                      "splitflag": split_flag, "regflag": reg_flag, "time": time.ctime()})
                        except: pass
        return download_link

    #处理验证码                       
    def deal_split(self, code_handler, image):
        list_split_image = code_handler.main_deal_split(image)
        return list_split_image

    #识别
    def reg_code(self, list_split_image):
        all_plain_text = "0123456789abcdef"
        reg_plain_text = []
        neural = NeuralWork()
        list_input_data = []
        for each_split_image in list_split_image:
            each_input_data = []
            for x in xrange(each_split_image.size[1]):
                for y in xrange(each_split_image.size[0]):
                    if each_split_image.getpixel((y, x)):
                        each_input_data.append(0)
                    else:
                        each_input_data.append(1)
            list_input_data.append(each_input_data)
        out = neural.reg_net(list_input_data)
        for each in out:
            plain_text = int(round(each[0] * 100))
            if plain_text < 16:
                reg_plain_text.append(all_plain_text[plain_text])
        return reg_plain_text

        
#模拟浏览器
class DoSplinter(object):
    def __init__(self):
        self.browser = Browser("phantomjs")

    #访问网页
    def get_html(self, url):
        return self.browser.visit(url)


if __name__ == "__main__":
    conn = pymongo.Connection("127.0.0.1", 27017)
    db = conn["captchaimg"] 
    down_url = "http://www.drugfuture.com/cnpat/cn_patent.asp"
    patentno = "CN201310723026"
    down_patent = DownPatent(db, down_url)
    download_link = down_patent.download(patentno)
    print download_link
