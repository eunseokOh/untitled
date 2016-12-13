#-*- encoding:utf-8 -*-
import threading, mechanize, Queue
import urllib2, math
import urllib
from bs4 import BeautifulSoup

query = "추위사냥"

class YPIMcrawler_login(threading.Thread):
    def __init__(self, queue, url, header, search_tag, search_attr, search_key, id_tag, pass_tag, id_, pass_):
        threading.Thread.__init__(self)
        self.in_url = url
        self.header = header
        self.search_tag = search_tag
        self.search_attr = search_attr
        self.search_key = search_key
        self.id_tag = id_tag
        self.pass_tag = pass_tag
        self.id_ = id_
        self.pass_ = pass_
        self.queue = queue

    def run(self):
        browser = mechanize.Browser()
        browser.set_handle_robots(False)
        cookies = mechanize.CookieJar()
        browser.set_cookiejar(cookies)
        browser.addheaders = self.header
        browser.set_handle_refresh(False)

        browser.open(self.in_url)

        browser.select_form(nr=0)
        browser.form[self.id_tag] = self.id_
        browser.form[self.pass_tag] = self.pass_
        browser.submit()

        self.queue.put(browser)

class YPIMcrawler_nonlogin(threading.Thread):
    def __init__(self, queue, url, header, search_tag, search_attr, search_key, or_=False):
        threading.Thread.__init__(self)
        self.url = url
        self.header = header
        self.search_tag = search_tag
        self.search_attr = search_attr
        self.search_key = search_key
        self.queue = queue
        self.or_ = or_

    def run(self):

        if (self.header != None):
            request = urllib2.Request(self.url, headers=self.header)
            html = urllib2.urlopen(request)
        else:
            html = urllib2.urlopen(self.url)

        soup = BeautifulSoup(html.read(), "html.parser")

        if (self.search_attr.lower() == 'id'):
            soup_data = soup.find(self.search_tag, {self.search_attr:self.search_key})

        elif (self.or_ == True):
            soup_data = soup.find_all(True, {self.search_attr:self.search_key})

        elif (self.search_attr != None):
            soup_data = soup.find_all(self.search_tag, {self.search_attr, self.search_key})
        else:
            soup_data = soup.find_all(self.search_tag)

        self.queue.put(soup_data)

#<-----------------------------------------------

class ddanzi_find(threading.Thread):
    def __init__(self, return_queue, board):
        threading.Thread.__init__(self)
        global query
        self.url = "http://www.ddanzi.com/index.php?act=IS&is_keyword="+query+"&search_target="+board

        self.return_queue = return_queue
        req_queue = Queue.Queue()
        YPIMcrawler_nonlogin(req_queue, self.url, None, "div", "id", "AllWrap").start()  # class
        self.data = req_queue.get()
        #print self.data

    def run(self):
        print self.data
        """
        for i in self.data.find('h3',{'class','subTitle'}):
            return_list = []
            count_article = i.text.encode('utf-8')
            if(count_article.find('문서') >= 0):
                #--> find는 괄호안에 문자가 있으면 해당 위치 인덱스를 리턴 없으면 -1 리턴
                print i.span.text.strip('(|)')
                #--> strip : 양쪽 문자제거, |기호는 or, '('혹은 ')'를 양쪽에 있으면 제거하라는 의미
        """
            #spl = count_article.replace('(',"")
            #print spl


class ddanzi_paging_find(threading.Thread):
    def __init__(self, url, page):
        threading.Thread.__init__(self)
        req_queue = Queue.Queue()
        YPIMcrawler_nonlogin(req_queue, url+str(page), None, "div", "class", "AllWrap").start()  # class
        self.data = req_queue.get()

    def run(self):
        return_list =[]
        for i in self.data:
            if __name__ == '__main__':
                for j in i.findAll('dt'):  # title + href
                    #print j.a.text + j.a['href']
                    return_list.append({'title': j.a.text, 'href': j.a['href']})
                    #return self.return_queue.put(return_list)
                    #--> queue는 리턴할 필요 없음
                    #self.return_queue.put(return_list) 형식으로 사용
                    #return_queue를 ddanzi_paging_find 클래스 인스턴스 사용 시 넘겨 받을 것!

        for i in return_list:
            for j in i.keys():
                pass
                #print i[j]



board_list = ["content", "nick_name", "title"]
for i in board_list:
    queue = Queue.Queue()
    ddanzi_find(queue, i).start()
    #print queue.get()