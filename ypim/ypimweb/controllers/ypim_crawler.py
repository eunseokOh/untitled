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
        try:
            if (self.header != None):
                request = urllib2.Request(self.url, headers=self.header)
                html = urllib2.urlopen(request)
            else:
                html = urllib2.urlopen(self.url)

            soup = BeautifulSoup(html.read(), "html.parser")

            if (self.search_attr.lower() == 'id'):
                soup_data = soup.find(self.search_tag, {self.search_attr, self.search_key})

            elif (self.or_ == True):
                soup_data = soup.find_all(True, {self.search_attr: self.search_key})

            elif (self.search_attr != None):
                soup_data = soup.find_all(self.search_tag, {self.search_attr, self.search_key})
            else:
                soup_data = soup.find_all(self.search_tag)

            self.queue.put(soup_data)
        except:
            print self.url + " open error"


### facebook start ###

class find_facebook(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        # req_class, url, header, search_tag, search_attr, search_key, id_tag, pass_tag, id_, pass_
        self.url = 'http://www.facebook.com/login.php'
        self.header = [('user-agent',
                        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36')]
        self.id_ = "experiment9090@gmail.com"
        self.pass_ = "ypim9090"
        queue = Queue.Queue()


        # self, queue, url, header, search_tag, search_attr, search_key, id_tag, pass_tag, id_, pass_
        YPIMcrawler_login(queue, self.url, self.header, None, None, None, 'email', 'pass', self.id_, self.pass_).start()

        self.broswer = queue.get()

    def run(self):
        global query, conn, lock

        url = "https://www.facebook.com/search/str/" + query + "/keywords_users"
        resp = self.broswer.open(url)  # data = set_cookie_broswer (cookie 값 저장됨)
        html = str(resp.read()).replace("<!--", "").replace("-->", "")
        Soup = BeautifulSoup(html, "html.parser")
        db = model.model(conn)
        # print Soup.prettify()
        data_list = Soup.find_all('div', {"class", "_glj"})
        return_facebook_list = []

        for i in data_list:
            each_data = i.find('div', {"class", "_gll"})
            each_name = each_data.text
            each_url = each_data.a['href']

            each_data = i.find('div', {"class", "_glm"})
            job = each_data.text

            each_data = i.find('div', {"class", "_glo"})
            school = each_data.text

            # title = each_name + ", " +  + ", " + job + ", " + school

            title = each_name + "/ " + job + "/ " + school
            img = "http://www.boatshop24.co.uk/upload/Facebook.png"
            lock.acquire()
            face_data = {"web_site":"facebook","href": each_url, "title": title, "img":img}
            db.tb_detail_insert(query,face_data)
            lock.release()

        print "facebook_end"


## end facebook ##

## 조선 일보 ##
class chosun_find(threading.Thread):
    def __init__(self, board):
        threading.Thread.__init__(self)
        global query
        self.url = "http://search.chosun.com/search/" + board + ".search?query=" + query + "&pageno="
        #
        # self.page = str(page)
        req_queue = Queue.Queue()
        YPIMcrawler_nonlogin(req_queue, self.url, None, "div", "class", "result_box").start()  # class
        self.data = req_queue.get()

    def run(self):
        print "chosun_find"
        # req_class, url, header, search_tag, search_attr, search_key
        return_list = []

        for i in self.data:

            try:
                count_article = i.h3.em.text.strip('(').encode('utf-8')
                spl = count_article.index('건')  # total page url - wikidocs.net/13
                n_cnt_article = int(count_article[:spl])
                total_page_no = int(math.ceil(n_cnt_article / 10.0))  # casting

                now_page = 1
                end_page_no = 1
                db = model.model(conn)

                while (True):
                    if (now_page > total_page_no):
                        break
                    else:
                        print "chosun_find_threading..."
                        chosun_paging_find(self.url, now_page, db).start()

                    now_page += 1
                    end_page_no += 1

                    if (end_page_no == 11):
                        end_page_no = total_page_no
                        break

            except:
                print "chosun Error"
                pass



class chosun_paging_find(threading.Thread):
    def __init__(self,  url, page, db):
        threading.Thread.__init__(self)
        req_queue = Queue.Queue()
        YPIMcrawler_nonlogin(req_queue, url + str(page), None, "div", "class", "result_box").start()  # class
        self.data = req_queue.get()
        self.db = db
    def run(self):
        global query,lock

        for i in self.data:
            for j in i.section.findAll('dt'):  # title + href
                img ="http://a687.phobos.apple.com/us/r30/Purple4/v4/1c/cd/c4/1ccdc467-74ba-7c09-7fd9-ea312afd56ba/mzl.dgttzlmr.png"
                lock.acquire()
                chosun_data = {"web_site": "chosun", "href": j.a['href'], "title": j.text, "img": img}
                self.db.tb_detail_insert(query, chosun_data)
                lock.release()




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



