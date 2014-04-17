__author__ = "happyin3"
#coding: utf-8

import time
import urllib
from splinter import Browser


class DownCode(object):
    def __init__(self):
        self.browser = Browser("phantomjs")

    def get_html(self, url):
        self.browser.visit(url)
        return self.browser

    def get_img_path(self, url, number):
        list_save_path = []
        for i in xrange(0, number):
            print i
            browser = self.get_html(url)
            browser_form = browser.find_by_tag("form")
            browser_img = browser_form.find_by_tag("img").first

            save_path = "static/images/downcode/" + time.ctime() + ".png"
            save_path_temp = "../%s" % save_path
            urllib.urlretrieve(browser_img["src"], save_path_temp)
            list_save_path.append(save_path)

            time.sleep(1)
        return list_save_path

    def get_captcha(self, code_img):
        list_save_path = []
        for path in code_img:
            img_name = "static/images/downcode/" + time.ctime() + ".png"
            img_name_temp = "../%s" % img_name
            urllib.urlretrieve(path, img_name_temp)
            list_save_path.append(img_name)             
            time.sleep(1) 
        return list_save_path

    def main(self, url, number):
        list_save_path = self.get_img_path(url, number)
        #list_save_path = self.get_captcha(code_img)
        
        return list_save_path


if __name__ == "__main__":
    url = "http://www.drugfuture.com/cnpat/verify.aspx"
    number = 500
    down = DownloadCaptcha()
    down.main(url, number)
    print "Nice"

