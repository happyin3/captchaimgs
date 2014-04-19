__author__ = "happyin3"
#coding: utf-8

import sys
import socket
import urllib
import time
import pymongo
from splinter import Browser 


#文件格式转换
class ConvertClient(object):
    def __init__(self, down_url, server_address, convert_url):
        self.down_url = down_url
        self.server_address = (server_address[0], int(server_address[1]))
        self.convert_url = convert_url

    #连接服务器，转换格式
    def connect_server(self, pdf_url):
        list_save_name = []
        #获取PDF下载地址
        splinter_thesis = SplinterThesis()
        down_url = splinter_thesis.main(self.down_url, pdf_url)
        #下载地址查找正确
        if len(down_url):
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect(self.server_address)

            try:
                sock.sendall(down_url)

                sock.sendall("eof")

                #接受数据
                buf = ""
                while True:
                    temp_buf = sock.recv(1024)
                    if not len(temp_buf):
                        break
                    buf += temp_buf

                #PDF下载失败
                if len(buf):
                    list_img = buf.split("?")
            
                    #下载图片
                    server_head = self.convert_server
                    for i in xrange(len(list_img)-1):
                        each_img = list_img[i]
                        img_path = server_head + each_img
                        save_name = self.download_img(img_path)
                
                        list_save_name.append(save_name)
            except:
                pass
            finally:
                sock.close()

        return list_save_name

    #下载图片
    def download_img(self, img_path):
        save_name = "static/images/convertimg/" + time.ctime() + ".jpg"
        save_name_temp = "../%s" % save_name
        urllib.urlretrieve(img_path, save_name_temp)
        time.sleep(1)
        
        return save_name


#获取下载地址        
class SplinterThesis(object):
    def __init__(self):
        self.browser = Browser("phantomjs")
    
    #访问网页
    def get_html(self, url):
        self.browser.visit(url)
        return self.browser
    
    #查找下载地址
    def get_down_url(self, down_url, browser):
        result = browser.find_link_by_text("下载全文")
        down_url = ""
        if result:
            result = str(result["onclick"]).split("'")
            temp_url = down_url + result[1]
            browser.visit(temp_url)
            result = browser.find_link_by_text("下载地址")
        
            if browser and result["href"]:
                down_url = result["href"]
        
        return down_url

    def main(self, down_url, url):
        html_url = down_url + url
        browser = self.get_html(html_url)
        down_url = self.get_down_url(down_url, browser)
        return down_url
        
