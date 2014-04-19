__author__ = "happyin3"
#coding: utf-8

import time
from PIL import Image
from splinter import Browser

from codeclass import CodeHandler
from codeclass import NeuralWork


#下载专利
class DownPatent(object):
    def __init__(self, down_url):
        self.down_url = down_url
        self.browser = Browser("phantomjs")

    #下载专利
    def download(self, db):
        #访问网页
        #网页加载超时
        #down_flag, 0：未下载，1：不存在，2：下载失败
        down_flag = 0
        for page_num in xrange(10):
            self.browser.visit(self.down_url)
            if not self.browser.is_element_not_present_by_value("查询", wait_time=10):
                #填写专利号
                self.browser.fill("cnpatentno", patentno)
                self.browser.find_by_value("查询").first.click()

                #连接超时，404
                if self.browser:
                    #一个最多循环20次
                    code_handler = CodeHandler()
                    for code_num in xrange(20):
                        #查找验证码
                        if not self.browser.is_element_not_present_by_id("getcode", wait_time=5)
                            #截图
                            self.browser.driver.maximize_window()
                            self.browser.driver.save_screenshot("scerrnshot.png")
                            #获取验证码图片
                            image = Image.open("screenshot.png")
                            image_code = image.crop((3,50, 55, 71))
                            save_path = "static/images/onlinecode/" + time.ctime() + ".png"
                            save_path_temp = "../%s" % save_path
                            image_code.save(save_path_temp)
                            
                            #分割图片
                            list_split_image = self.deal_split(image_code)
                            
                            #识别，如果能正确识别，则识别，不能，则重新获取验证码      
                            if len(list_split_image) == 4:
                                reg_plain_text = self.reg_code(list_split_image)
                                fill_text = "".join(reg_plain_text)

                                #填写验证码
                                self.browser.fill("ValidCode", fill_text)
                                self.browser.find_by_value("确定").first.click()

                                #判断识别结果 
                                down_none = self.browser.find_by_text("没有找到该专利!请检查输入的专利号或公开号是否正确!")
                                if not down_none:
                                    down_link_one = self.browser.find_link_by_text("申请公开说明书图形下载(标准版)")
                                    down_link_two = self.browser.find_link_by_text("申请公开说明书图形下载(极速版)")
                                    if down_link_one or down_link_two:
                                        if down_link_one:
                                            self.browser.click_link_by_text("申请公开说明书图形下载(标准版)")
                                        else:
                                            self.browser.click_link_by_text("申请公开说明书图形下载(极速版)")
                                    elif down_none:
                                        browser.back()
                                        browser.reload()
                                else:
                                    #没有专利
                                    down_flag = 1
                                    break
                            else:
                                #存数数据集onlinecode，验证码路径，识别次数，识别码，识别标志，不可分标志
                                try:
                                    self.db.onlinecode.insert({"codepath": save_path, "number": 0, "regtext": [], "regflag": 0, "splitflag": 1})
                                except: pass
                                browser.reload()
                   
                    #没有专利，跳出循环
                    if down_flag == 1:
                        break 
        
        #下载判断
        

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

    #查找下载专利
    def find_downurl(self):
        
#模拟浏览器
class DoSplinter(object):
    def __init__(self):
        self.browser = Browser("phantomjs")

    #访问网页
    def get_html(self, url):
        return self.browser.visit(url)

