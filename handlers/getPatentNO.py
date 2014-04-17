__author__ = "happyin3"
#coding: utf-8


import urllib
import urllib2


class GetPatentNO(object):
    def __init__(self):
        pass

    def send_post(self):
        try:
            params = urllib.urlencode({"patentno": "3"})
            request = urllib2.Request("http://172.16.111.230:8888/getImageUrl", params)
            response = urllib2.urlopen(request)
            print response.read()
        except Exception, e:
            print e


if __name__ == "__main__":
    get_patent = GetPatentNO()
    get_patent.send_post()
