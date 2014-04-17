__author__ = "happyin3"
#coding: utf-8

import sys
import socket
import urllib
import time
import pymongo
from splinter import Browser


class ConvertClient(object):
    def __init__(self):
        pass

    def connect_server(self, pdf_url):
        list_save_name = []
        splinter_thesis = SplinterThesis()
        down_url = splinter_thesis.main(pdf_url)
        if len(down_url):
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            #server_address = ("210.29.152.145", 8889)
            server_address = ("172.16.111.230", 8889)
            sock.connect(server_address)

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
                if buf:
                    list_img = buf.split("?")
            
                    #下载图片
                    #server_head = "http://signals.hyit.edu.cn:8080/convertserver"
                    server_head = "http://172.16.111.230:8080/convertserver"
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

    def download_img(self, img_path):
        save_name = "static/images/convertimg/" + time.ctime() + ".jpg"
        save_name_temp = "../%s" % save_name
        urllib.urlretrieve(img_path, save_name_temp)
        time.sleep(1)
        
        return save_name

        
class SplinterThesis(object):
    def __init__(self):
        self.browser = Browser("phantomjs")
        #self.browser = Browser()

    def get_html(self, url):
        self.browser.visit(url)
        return self.browser

    def get_down_url(self, browser):
        #if not browser.is_element_not_present_by_tag("a", wait_time=6):
        result = browser.find_link_by_text("下载全文")
        down_url = ""
        if result:
            result = str(result["onclick"]).split("'")
            temp_url = "http://202.195.136.17" + result[1]
            browser.visit(temp_url)
            result = browser.find_link_by_text("下载地址")
        
            if browser and result["href"]:
                down_url = result["href"]
        
        return down_url

    def main(self, url):
        html_url = "http://202.195.136.17" + url
        browser = self.get_html(html_url)
        down_url = self.get_down_url(browser)
        return down_url
        
