__author__ = "happyin3"
#coding: utf-8

import pymongo
from PIL import Image

def change_file_name(db):
   
    #读取数据集mergeimg，获取indexflag和mergepath
    results = db.mergeimg.find({}, {"_id": 0, "indexflag": 1, "mergepath": 1})
    #是否有数据
    if results:
        #替换文件名
        for result in results:
            thesis_url = result["indexflag"]
            merge_path = result["mergepath"]
            thesis_urls = thesis_url.split("/")
            thesisno = thesis_urls[len(thesis_urls)-1][:-5]
             
            #读取图片
            if len(merge_path):
                try:
                    image = Image.open("../%s" % merge_path)
                    save_path = "static/images/mergeimg/" + thesisno + ".jpg"
                    #保存图片
                    image.save("../%s" % save_path)
                    #更新数据集
                    db.mergeimg.update({"indexflag": thesis_url}, {"$set": {"mergepath": save_path}})
                    print "nice"
                except: pass
            print thesisno
    
    '''
    #读取数据集urlno，获取indexflag和mergepath
    results = db.urlno.find({"kind": "patent", "extractflag": 1}, {"_id": 0, "indexflag": 1, "mergepath": 1})
    #是否有数据
    if results:
        #替换文件名
        for result in results:
            patentno = result["indexflag"]
            merge_path = result["mergepath"]

            #读取图片
            if len(merge_path):
                try:
                    print merge_path
                    image = Image.open("../%s" % merge_path)
                    save_path = "static/images/mergeimg/" + patentno + ".jpg"
                    #保存图片
                    image.save("../%s" % save_path)
                    #更新数据集
                    db.urlno.update({"indexflag": patentno}, {"$set": {"mergepath": save_path}})
                    print "Nice"
                except Exception, e: print e
            print patentno
    '''

if __name__ == "__main__":
    conn = pymongo.Connection("127.0.0.1", 27017)
    db = conn["captchaimg"]
    change_file_name(db)
