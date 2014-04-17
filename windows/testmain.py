__author__ = "happyin3"
#coding: utf-8

import pymongo
import time
from PIL import Image

from getremote import GetUrl
from convertclient import ConvertClient
from extractimg import ExtractImage


class MainHandler(object):
    def __init__(self):
        pass
 
    #远程获取url
    def get_url(self):
        geturl = GetUrl()
        list_url = geturl.get_url()
   
    #转换图片格式 
    def convert_image(self):
        list_pdf_url = []
        list_pdf_url.append("http://signals.hyit.edu.cn/papers/%E6%B4%AA%E6%B3%BD%E6%B9%96%E6%B0%B4%E4%BD%8D%E9%A2%84%E6%B5%8B%E6%A8%A1%E5%9E%8B%E7%9A%84%E7%A0%94%E7%A9%B6.pdf")
        list_pdf_url.append("http://signals.hyit.edu.cn/papers/2009%2010th%20ACIS-SNPD.pdf")
        list_pdf_url.append("http://signals.hyit.edu.cn/papers/%E5%9F%BA%E4%BA%8EJ2ME%E7%9A%84%E7%A7%BB%E5%8A%A8%E7%BD%91%E7%BB%9C%E6%B3%A1%E6%B3%A1%E5%A0%82%E6%B8%B8%E6%88%8F%E7%B1%BB%E8%AE%BE%E8%AE%A1.pdf")

        #下载PDF，并转成图片
        convert_client = ConvertClient()
        for pdf_url in list_pdf_url:
            print pdf_url
            list_save_name = convert_client.connect_server(pdf_url)
            self.extract_image(list_save_name)

    #提取图片        
    def extract_image(self, list_convert_img):    
        #提取图片
        list_save_path = []
        for convert_img in list_convert_img:
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
            if each_save_path[0][1]:
                list_merge_image_path.append(each_save_path[0][1])
            if len(each_save_path[0][2]):
                for each_extract_image_path in each_save_path[0][2]:
                    list_extract_image_path.append(each_extract_image_path)
        #合并单页图片
        list_merge_image = []
        for each_merge_image_path in list_merge_image_path:
            image = Image.open(each_merge_image_path)
            list_merge_image.append(image)

        extract_img = ExtractImage() 
        final_merge_image_path = extract_img.image_merge(list_merge_image)
        
    def main(self):     
        self.convert_image()


if __name__ == "__main__":
    main_handler = MainHandler()
    main_handler.main()
           
