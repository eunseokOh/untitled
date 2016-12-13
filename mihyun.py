#-*- encoding:utf-8 -*-
import multiprocessing as mp, mechanize, threading, Queue
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

class YPIMcrawler_nonlogin(mp.Process):
    def __init__(self, queue, url, header, search_tag, search_attr, search_key, or_=False):
        mp.Process.__init__(self)
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
            soup_data = soup.find(self.search_tag, {self.search_attr, self.search_key})

        elif (self.or_ == True):
            soup_data = soup.find_all(True, {self.search_attr:self.search_key})

        elif (self.search_attr != None):
            soup_data = soup.find_all(self.search_tag, {self.search_attr, self.search_key})
        else:
            soup_data = soup.find_all(self.search_tag)
        print "11"
        self.queue.put(soup_data)

#<-----------------------------------------------

class ddanzi_find(threading.Thread):
    def __init__(self, return_queue):
        threading.Thread.__init__(self)
        global query
        self.url = "http://www.ddanzi.com/index.php?mid=ddanziMain&act=IS&search_target=all&is_keyword="+query+"&where=document&page="

        self.return_queue = return_queue
        req_queue = mp.Queue()
        YPIMcrawler_nonlogin(req_queue, self.url, None, "h3","class","subTitle").start()  # class
        self.data = req_queue.get()

        #print self.data
    def run(self):
        return_list = []
        for i in self.data:
            try:
                count_article = i.text.encode('utf-8')
                if (count_article.find('문서') >= 0):
                    n_cnt_article = int(i.span.text.encode('utf-8').strip('(|)'))
                    total_page_no = int(math.ceil(n_cnt_article / 30.0))

                    if (total_page_no >= 10):
                        total_page_no = 10

                    now_page = 1
                    while(True):
                        if (now_page > total_page_no):
                            break
                        else:
                            ddanzi_paging_find(self.url, now_page).start()
                        now_page+=1
            except:
                print "error?"
                pass

        self.return_queue.put(return_list)

class ddanzi_paging_find(threading.Thread):
    def __init__(self, url, page):
        threading.Thread.__init__(self)

        mp_que = mp.Queue()
        YPIMcrawler_nonlogin(mp_que, url+str(page), None, "div","class","mainActWrap").start()  # class
        self.data = mp_que.get()
        print url

    def run(self):
        return_list =[]
        for i in self.data:
            for j in i.findAll('ul', {'class': 'searchResult'}):
                for j_ in j.findAll('dt'):
                    #print j_.a.text + " = " + j_.a['href']
                    return_list.append({'title': j_.a.text, 'href': j_.a['href']})

        for i in return_list:
            for j in i.keys():
                #pass
                print i[j]


if __name__ == '__main__':
    queue = Queue.Queue()
    ddanzi_find(queue).start()
    #print queue.get()