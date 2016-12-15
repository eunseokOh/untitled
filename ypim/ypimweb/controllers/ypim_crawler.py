# -*- encoding:utf-8 -*-

from bs4 import BeautifulSoup
import mechanize, urllib2, threading, Queue, math
import multiprocessing as mp
from ypim.ypimweb.models import db_conn, model

query = None
conn = None

class href_preview(threading.Thread):
    def __init__(self, queue, url, broswer=None):
        threading.Thread.__init__(self)
        self.url = url
        self.queue = queue
        self.broswer = broswer
        # print self.url

    def run(self):
        try:
            if (self.broswer != None):
                html = self.broswer.open(self.url).read().replace("<!--", "<").replace("-->", ">")
            else:
                html = urllib2.urlopen(self.url).read().replace("<!--", "<").replace("-->", ">")
            soup = BeautifulSoup(html, "html.parser")
            pre_make_list = []
            return_list = []
            meta_title = soup.find_all(["meta", "title"])

            title_input_count = 0

            for i in meta_title:
                try:
                    if (title_input_count == 0):
                        title = i.find('title').text
                        pre_make_list.append({"main_title": title})
                        title_input_count = 1
                    pre_make_list.append({i['property']: i['content']})

                except:
                    pass

            for i in pre_make_list:
                for j in i.keys():
                    try:
                        if (j.find('main') >= 0):
                            return_list.append({"main_title": i[j]})
                        elif (j.find('tit') >= 0):
                            return_list.append({"title": i[j]})
                        if (j.find("im") >= 0):
                            return_list.append({"img": i[j]})
                        if (j.find('des') >= 0):
                            return_list.append({"description": i[j]})
                    except:
                        print "preview parsing error"
                        pass
            self.queue.put(return_list)
        except:
            print self.url + " url open error"
            pass


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
        try:
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
        except:
            print "broswer error"

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
            soup_data = soup.find(self.search_tag, {self.search_attr, self.search_key})

        elif (self.or_ == True):
            soup_data = soup.find_all(True, {self.search_attr:self.search_key})

        elif (self.search_attr != None):
            soup_data = soup.find_all(self.search_tag, {self.search_attr, self.search_key})
        else:
            soup_data = soup.find_all(self.search_tag)

        self.queue.put(soup_data)

## 조선 일보 END ##

## crawler_pre
def ypim_crawler_facebook():
    print "facebook_run"
    find_facebook().start()


def ypim_crawler_chosun():
    board_list = ["news", "infomain", "photo", "movie", "community", "person", "qna"]
    print "chosun_run"
    for i in board_list:
        chosun_find(i).start()
### end

def init(query_):
    global conn, query, lock

    db = db_conn.db_conn()
    conn = db.db_conn()
    query = query_
    lock = threading.Lock()

class ypim_crawler():
    def __init__(self, query_):
        self.query = query_.encode("utf-8")

        db = db_conn.db_conn()
        self.conn = db.db_conn()

    def run(self):
        db = model.model(self.conn)
        result = db.tb_query_select(self.query)
        seq_que = result[0]['que_seqno']

        if(seq_que == None):
            db.tb_query_insert(self.query)

            crawler_class_list =  [ypim_crawler_chosun, ypim_crawler_facebook]
            try:

                pool = mp.Pool(initializer=init, initargs=(self.query,))
                for i in crawler_class_list:
                    p = pool.apply_async(i)
                    p.ready()


            except Exception as e:
                print e

            finally:
                self.conn.close()
                return "crawler"

        else:
            query_list = db.tb_detail_select(seq_que)
            print query_list
            #print db_list
            self.conn.close()
            return query_list

if __name__ == '__main__':
    mp.freeze_support()

        # return return_list



