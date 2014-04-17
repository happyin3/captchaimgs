__author__ = "happyin3"
#coding: utf-8

import time
import urllib
from splinter import Browser
from dealcode import DealImage 
from neuralwork import NeuralWork


class DoSplinter(object):
    def __init__(self):
        self.browser = Browser("phantomjs")
        #self.browser = Browser()

    #打开页面
    def get_html(self, url):
        self.browser.visit(url)
        return self.browser

    #获取验证码图片
    def get_code(self, url, patentno):
        browser = self.get_html(url)
        #填写专利号
        browser.fill("cnpatentno", patentno)
        browser.find_by_value("查询").first.click()
        
        #连接超时，404
        if browser:
            #一个最多循环20次
            for i in xrange(20):
                #查找验证码
                if not browser.is_element_not_present_by_id("getcode", wait_time=5):
                    browser_img = browser.find_by_id("getcode")
                    code_img = ""
                    if browser_img:
                        code_img = browser_img["src"]

                    #下载验证码
                    save_path = ""
                    if len(code_img):
                        save_path = "static/images/onlinecode/" + time.ctime() + ".png"
                        save_path_temp = "../%s" % save_path
                        urllib.urlretrieve(code_img, save_path_temp)
           
                        #分割图片 
                        list_split_image = self.deal_split(save_path_temp)
            
                        #识别，如果能正确分割，则识别，不能，则重新获取验证码
                        if len(list_split_image) == 4:
                            #一个最多识别10次
                            reg_plain_text = self.reg_code(list_split_image)
                            fill_text = "".join(reg_plain_text)

                            print fill_text, save_path
                            #填写验证码
                            browser.fill("ValidCode", fill_text)
                            browser.find_by_value("确定").first.click()

                            #判断识别结果
                            down_link_one = browser.find_link_by_text("申请公开说明书图形下载(标准版)")
                            down_link_two = browser.find_link_by_text("申请公开说明书图形下载(极速版)")
                            if down_link_one or down_link_two:
                                if down_link_two:
                                    browser.click_link_by_text("申请公开说明书图形下载(极速版)")
                                    print browser.html
                            else:
                                browser.back()
                        else:
                            #刷新，重新获取验证码
                            browser.reload()
        return

    def deal_split(self, save_path): 
        #处理分割图片
        deal_code = DealImage() 
        list_split_image = deal_code.main_deal_split(save_path)
        
        return list_split_image

    def reg_code(self, list_split_image):
        #识别
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
               
    def main(self, url, patentno):
        print "getcode"
        self.get_code(url, patentno)
        

if __name__ == "__main__":
    url = "http://www.drugfuture.com/cnpat/cn_patent.asp"
    patentno = "CN201310638017"
    do_splinter = DoSplinter()
    do_splinter.main(url, patentno)
