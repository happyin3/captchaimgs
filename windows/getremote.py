__author__ = "happyin3"
#coding: utf-8

import pysolr

class GetUrl(object):
    def __init__(self):
        self.solr = pysolr.Solr("http://localhost:8983/solr/papers", timeout=10)
        pass

    def get_url(self, start, rows=100):
        results = self.solr.search("*:*", start=start, rows=rows)
        list_url = []
        for result in results:
            list_url.append(result["path"])
        return list_url


class GetPatentNO(object):
    def __init__(self):
        pass

    def get_patentno(self):
        list_patentno = []
        return list_patentno


if __name__ == "__main__":
    geturl = GetUrl()
    results = geturl.get_url()
    for result in results:
        print result["path"]
