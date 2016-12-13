#-*- encoding:utf-8 -*-
import threading
import urllib2
import urllib
from bs4 import BeautifulSoup

query = "고등어사령관"
class YPIMcrawler(threading.Thread):
    def __init__(self, req_class, url, header, search_tag, search_attr, search_key):
        threading.Thread.__init__(self)
        self.url = url
        self.header = header
        self.search_tag = search_tag
        self.search_attr = search_attr
        self.search_key = search_key
        self.req_class = req_class


    def run(self):
        try:
            if (self.header != None):   #CookieVal
                request = urllib2.Request(self.url, headers=self.header)
                html = urllib2.urlopen(request)
            else:
                html = urllib2.urlopen(self.url)

            soup = BeautifulSoup(html.read(), "html.parser")

            if(self.search_attr != None):
                soup_data = soup.find_all(self.search_tag, {self.search_attr, self.search_key})
            else:
                soup_data = soup.find_all(self.search_tag)

            req_cls = self.req_class
            req_cls.get_data(soup_data)

            return soup_data


        except:
            print "error"
            next



class chosun_find(threading.Thread):
    def __init__(self, board):
        threading.Thread.__init__(self)
        global query
        self.url = "http://search.chosun.com/search/"+board+".search?query="+query+"&pageno="
        self.board = board
    def run(self):
        #req_class, url, header, search_tag, search_attr, search_key
        page_no = 1
        while(page_no <= 3):
            status = YPIMcrawler(self, self.url + str(page_no), None, "div", "class","result_box").start()
            print status
            page_no += 1


    def get_data(self, data):
        for i in data:
            for j in i.section.find_all('dl'):
                #print j.dt
                next



board_list = ["community"]#["news","infomain","photo","movie","community","person","qna"]
for i in board_list:
    chosun_find(i).start()
