#-*- encoding:utf-8 -*-

from bs4 import BeautifulSoup
import mechanize, urllib2, threading, Queue, math, urllib
from ypim.ypimweb.models import db_conn, model


query = None
conn = None

def init(query_):
    global conn, query, lock

    conn = db_conn.db_conn()
    query = query_
    lock = threading.Lock()

######################################################################

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
                        #print "chosun_find_threading..."
                        chosun_paging_find(self.url, now_page, db).start()

                    now_page += 1
                    end_page_no += 1

                    if (end_page_no == 4):
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
                img ="chosun.png"
                lock.acquire()
                chosun_data = {"web_site": "chosun", "href": j.a['href'], "title": j.text, "img": img}
                self.db.tb_detail_insert(query, chosun_data)
                lock.release()

## 조선 일보 END ##


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
            img = "facebook.png"
            lock.acquire()
            face_data = {"web_site":"facebook","href": each_url, "title": title, "img":img}
            db.tb_detail_insert(query,face_data)
            lock.release()

        print "facebook_end"


## end facebook ##

## 딴지 start ##

class ddanzi_find(threading.Thread):
    def __init__(self, board):
        threading.Thread.__init__(self)
        global query
        self.url = "http://www.ddanzi.com/index.php?act=IS&is_keyword="+query+"&search_target=all&where="+board+"&page="
        req_queue = Queue.Queue()
        YPIMcrawler_nonlogin(req_queue, self.url, None, "div","class","mainActWrap").start()  # class
        self.data = req_queue.get()
        #print self.data

    def run(self):
        global conn
        print "ddanzi_start"
        db = model.model(conn)
        for i in self.data:
            try:
                for j in i.findAll('h3', {'class': 'subTitle'}):
                    count_article = j.text.encode('utf-8')
                    if (count_article.find('문서') >= 0):
                        n_cnt_article = int(j.span.text.encode('utf-8').strip('(|)'))
                        total_page_no = int(math.ceil(n_cnt_article / 30.0))

                    if (total_page_no >= 3):
                        total_page_no = 3

                    now_page = 1
                    while(True):
                        if (now_page > total_page_no):
                            break
                        else:
                            ddanzi_paging_find(db,self.url, now_page).start()
                        now_page+=1
            except Exception as e:

                print e
                pass



class ddanzi_paging_find(threading.Thread):
    def __init__(self, db, url, page):
        threading.Thread.__init__(self)
        req_queue = Queue.Queue()
        YPIMcrawler_nonlogin(req_queue, url+str(page), None, "div","class","mainActWrap").start()  # class
        self.data = req_queue.get()
        self.db = db
    def run(self):
        global query, lock

        for i in self.data:
            for j in i.findAll('ul', {'class': 'searchResult'}):
                for j_ in j.findAll('dt'):
                    #print j_.a.text + " = " + j_.a['href']

                    img = "https://pbs.twimg.com/media/Bv4O-3iCYAAmFKs.jpg"
                    lock.acquire()
                    face_data = {"web_site": "ddanzi", "href": j_.a['href'], "title": j_.a.text, "img": img}
                    self.db.tb_detail_insert(query, face_data)
                    lock.release()

## 딴지 end ##

## 뽐뿌 start ##


class ppomppu_find(threading.Thread):
    def __init__(self, board):
        threading.Thread.__init__(self)
        global query
        self.url = "http://www.ppomppu.co.kr/search_bbs.php?search_type="+ board+"&keyword=" + unicode(query, 'utf-8').encode(
                'euc-kr') + "&page_no="
        # self.page = str(page)

        req_queue = Queue.Queue()
        YPIMcrawler_nonlogin(req_queue, self.url, None, "td", "id", "page_list").start()  # class
        self.data = req_queue.get()


    def run(self):
        global conn
        print "ppomppu_start"
        db = model.model(conn)

        for i in self.data:
            try:
                total_page_no = len(i.findAll('a'))

                if ( total_page_no >= 11 ):
                    total_page_no = 3
                else:
                    total_page_no = total_page_no+1


                if (total_page_no > 3):
                    total_page_no = 3

                now_page = 1
                while (True):
                    if (now_page > total_page_no):
                        break
                    else:
                        ppomppu_paging_find(db,self.url, now_page).start()
                    now_page += 1
            except Exception as e:
                print e
                pass

class ppomppu_paging_find(threading.Thread):
    def __init__(self, db, url, page):
        threading.Thread.__init__(self)
        req_queue = Queue.Queue()
        YPIMcrawler_nonlogin(req_queue, url+str(page), None, "div", "class", "container").start()  # class
        self.data = req_queue.get()
        self.db = db

    def run(self):
        global lock, query


        for i in self.data:
            for j in i.findAll('dt'):
                try:
                    href_article = str(j.a['href'])
                    if (href_article[7] == 'a'):
                        #print href_article[7]
                        pass
                    else:

                        img = "ppomppu.png"
                        lock.acquire()
                        face_data = {"web_site": "ppomppu", "href": href_article, "title": j.a.text, "img": img}
                        self.db.tb_detail_insert(query, face_data)
                        lock.release()
                except Exception as e:
                    print e
                    pass

## 뽐뿌 end ##

## 오유 start ##

#<-----------------------------------------------

class todayhumor_find(threading.Thread):
    def __init__(self, board):
        threading.Thread.__init__(self)
        global query
        self.url = "http://www.todayhumor.co.kr/board/list.php?&kind=search&keyfield="+board+"&keyword="+query+"&page=1"
        req_queue = Queue.Queue()
        header = {"user-agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36"}
        YPIMcrawler_nonlogin(req_queue, self.url, header, None, None, None).start()  # class
        self.data = req_queue.get()
        #print self.data

    def run(self):
        db = model.model(conn)
        total_page_no = -1
        for i in self.data:
            for j in i.findAll('td'):
                try:
                    if (j['align'] == "center"):
                        if (j['height'] == str(40)):
                            try:
                                if ( len(j.findAll('font')) > 0):
                                    total_page_no += len(j.findAll('font'))

                            except Exception as e:
                                print e

                            if (total_page_no >= 3):
                                total_page_no = 3

                            now_page = 1

                            while (True):
                                if (now_page > total_page_no):
                                    break
                                else:
                                    todayhumor_paging_find(db,self.url[:-1], now_page).start()

                                now_page += 1
                except:
                    pass

class todayhumor_paging_find(threading.Thread):
    def __init__(self, db,url, page):
        threading.Thread.__init__(self)
        req_queue = Queue.Queue()
        header = {"user-agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36"}
        YPIMcrawler_nonlogin(req_queue, url+str(page), header, None, None, None).start()  # class
        #print url+str(page)
        self.data = req_queue.get()
        self.db = db

    def run(self):
        global query, lock
        print "오유 run..."
        for i in self.data:
            for j in i.findAll('td'):
                try:
                    if (j['class'][0] == "subject"):
                        url2 =("http://www.todayhumor.co.kr" + j.a['href'])

                        img = "todayhumor.png"
                        lock.acquire()
                        face_data = {"web_site": "todayhumor", "href": url2, "title": j.text, "img": img}
                        self.db.tb_detail_insert(query, face_data)
                        lock.release()

                except:
                    pass


## 오유 end ##

## 클리앙 start ##
class clien_find(threading.Thread):
    def __init__(self, board):
        threading.Thread.__init__(self)
        global query
        self.url = "http://www.clien.net/cs2/bbs/zsearch.php?q="+query+"&category="+board+"&page="
        req_queue = Queue.Queue()
        YPIMcrawler_nonlogin(req_queue, self.url, None, "div", "class", "paging").start()  # class
        self.data = req_queue.get()


    def run(self):
        global conn
        print "clien_start"
        db = model.model(conn)

        for i in self.data:
            print
            try:
                total_page_no = len(i.findAll("a"))
                #print total_page_no
                print total_page_no
                if (total_page_no >= 3):
                    total_page_no = 3
                now_page = 1
                while (now_page <= total_page_no):
                    clien_paging_find(db, self.url, now_page).start()
                    now_page += 1

            except Exception as e:
                print e


class clien_paging_find(threading.Thread):
    def __init__(self, db, url, page):
        threading.Thread.__init__(self)
        req_queue = Queue.Queue()
        YPIMcrawler_nonlogin(req_queue, url + str(page), None, "div", None, None).start()  # class
        self.data = req_queue.get()
        self.db = db

    def run(self):
        global query, lock
        return_list = []
        for i in self.data:
            for j in i.findAll('div', {'class': 'post_subject'}):
                url2 = ("http://www.clien.net" + j.a['href'])
                #print url2
                img = "clien.png"
                lock.acquire()
                clien_data = {"web_site": "clien", "href": url2, "title": j.h4.text, "img": img}
                self.db.tb_detail_insert(query, clien_data)
                lock.release()

## 클리앙 end ##

## 디시인사이드 start ##
class dcinside_find(threading.Thread):
    def __init__(self, board):
        threading.Thread.__init__(self)
        global query
        self.url = "http://search.dcinside.com/"+board+"/q/"+query+"/p/"
        req_queue = Queue.Queue()
        YPIMcrawler_nonlogin(req_queue, self.url, None, "div","class","search-result-right").start()  # class
        self.data = req_queue.get()

    def run(self):
        global conn
        print "dcinside_start"
        db = model.model(conn)

        for i in self.data:
            max_page = None
            for j in i.findAll('div', {'id': 'dgn_btn_paging'}):
                max_page = len(j.findAll('a'))

            if (max_page > 3):
                max_page = 3
            now_page = 1
            while (now_page <= max_page):
                dcinside_paging_find(db,self.url, now_page).start()
                now_page += 1

class dcinside_paging_find(threading.Thread):
    def __init__(self, db, url, page):
        threading.Thread.__init__(self)
        req_queue = Queue.Queue()
        YPIMcrawler_nonlogin(req_queue, url + str(page), None, "div","class","search-result-right").start()  # class
        self.data = req_queue.get()
        self.db = db

    def run(self):
        global query, lock
        for i in self.data:
            for j in i.findAll('div', {'class': 'thumb_txt'}):
                #return_list.append({'title': j.text, 'href': j.a['href']})
                img = "dcinside.png"
                lock.acquire()
                dcinside_data = {"web_site": "dcinside", "href": j.a['href'], "title": j.text, "img": img}
                self.db.tb_detail_insert(query, dcinside_data)
                lock.release()

## 디시인사이드 end ##


## 엠팍 start ##
class mlbpark_find(threading.Thread):
    def __init__(self, board):
        threading.Thread.__init__(self)
        global query
        self.url = "http://mlbpark.donga.com/mlbpark/b.php?&m=search&b="+board+"&query="+"\""+query+"\""+"&select=sct&p="
        req_queue = Queue.Queue()
        YPIMcrawler_nonlogin(req_queue, self.url, None, None ,None ,None).start()  # class
        self.data = req_queue.get()

    def run(self):
        global conn
        print "mlbpark_start"
        db = model.model(conn)

        for i in self.data:
            for j in i.findAll('div',{'class','page'}):
                max_page = 0
                if (j.text):
                    max_page = len(j.findAll("a")) + 1
                    try:
                        if (max_page > 3):
                            max_page = 3
                        now_page = 1
                        else_page = 1
                        while (now_page <= max_page):
                            if(now_page == 1):
                                mlbpark_paging_find(db, self.url, now_page).start()
                            else:
                                else_page += 30
                                mlbpark_paging_find(db, self.url, else_page).start()
                            now_page += 1
                    except:
                        pass
                else:
                    break

class mlbpark_paging_find(threading.Thread):
    def __init__(self, db, url, page):
        threading.Thread.__init__(self)
        req_queue = Queue.Queue()
        YPIMcrawler_nonlogin(req_queue, url + str(page), None, None ,None ,None).start()  # class
        self.data = req_queue.get()
        self.db = db

    def run(self):
        global query, lock
        for i in self.data:
            for j in i.findAll('td', {'class', 't_left'}):
                if(j):
                    #return_list.append({'title': j.a.text, 'href': j.a['href'].replace("#","")})
                    img = "mlbpark.png"
                    if(j.a.text.replace(" ","") != ""):
                        #print j.a.text
                        lock.acquire()
                        mlbpark_data = {"web_site": "mlbpark", "href": j.a['href'].replace("#",""), "title": j.a.text, "img": img}
                        self.db.tb_detail_insert(query, mlbpark_data)
                        lock.release()

## 엠팍 end ##

## 도탁스 start ##

class DOTAX_find(threading.Thread):
    def __init__(self, board):
        threading.Thread.__init__(self)
        global query, conn #추가
        self.url = "http://cafe984.daum.net/_c21_/cafesearch?grpid=mEr9&listnum=50&head=&viewtype=all&searchPeriod=all&item="+board
        #html = urllib2.urlopen(self.url + board[1][1] + unicode(query, 'utf-8').encode('euc-kr')).read()

        req_queue = Queue.Queue()
        self.db = model.model(conn) # 추가

        YPIMcrawler_nonlogin(req_queue, self.url + unicode(query, 'utf-8').encode('euc-kr'), None,"tr", "class", "list_row_info").start()  # class
        self.data = req_queue.get()

    def run(self):
        # req_class, url, header, search_tag, search_attr, search_key
        for i in self.data:

            url2 = ("http://cafe984.daum.net" + i.a['href'])
            #print url2
            #print j.a.text + url2
            img = "dotax.PNG"
            dotax_data = {"web_site": "dotax", "href": url2, "title": i.a.text, "img": img}
            lock.acquire()
            self.db.tb_detail_insert(query, dotax_data)
            lock.release()

## 도탁스 end ##

## 잡코리아 start##
class jobkorea_find(threading.Thread):
    def __init__(self, board):
        threading.Thread.__init__(self)
        global query

        self.url = "http://www.jobkorea.co.kr/Search/Category?stext=" + query + "&param=" + board + "&Oem_Code=C1"
        print self.url
        req_queue = Queue.Queue()
        header = {"user-agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36"}
        YPIMcrawler_nonlogin(req_queue, self.url, header, None, None, None).start()  # class  "div", "class", "inner"
        self.data = req_queue.get()
        print self.data

    def run(self):
        global conn
        db = model.model(conn)
        max_page = 0
        try:
            for i in self.data:
                max_page = len(i.findAll('a'))
                print max_page
            if ( max_page > 3):
                max_page = 3

            now_page = 1
            while( now_page <= max_page):
                jobkorea_paging_find(db, self.url+"&page=", now_page).start()
                now_page += 1

        except Exception as e:
            print e

class jobkorea_paging_find(threading.Thread):
    def __init__(self, db, url, page):
        threading.Thread.__init__(self)
        req_queue = Queue.Queue()
        header = {"user-agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36"}
        YPIMcrawler_nonlogin(req_queue, url + str(page), header, "ul", "class", "detailList").start()  # class
        # print url+str(page)
        self.data = req_queue.get()
        self.db = db

    def run(self):
        global query, lock
        print "잡코리아 run..."
        for i in self.data:
            for j in i.findAll('li'):
                try:
                    img = "https://pbs.twimg.com/profile_images/1930939695/JOBKOREA_CI_400x400.png"
                    jobkorea_data = {"web_site": "jobkorea", "href": j.ul.li.a['href'], "title": j.text, "img": img}

                    lock.acquire()
                    self.db.tb_detail_insert(query, jobkorea_data)
                    lock.release()

                except:
                    pass

## 잡코리아 end##



## inven start ##

class inven_find(threading.Thread):
    def __init__(self, model, url, subjcont):
        global query
        self.model = model

        threading.Thread.__init__(self)
        self.url_ = url+"&keyword="+query+"&name="+subjcont
        self.header = {
            "user-agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36"}


    def run(self):
        global lock, query

        try:
            search_tag = "tr"
            search_attr = "class"
            search_key = "ls"
            or_ = False

            lock.acquire()
            if (self.header != None):
                request = urllib2.Request(url=self.url_, headers=self.header)
                html = urllib2.urlopen(request)
            else:
                html = urllib2.urlopen(self.url_)
            lock.release()

            soup = BeautifulSoup(html.read(), "html.parser")

            if (search_tag == None):
                soup_data = [soup]
            elif (or_ == True):
                soup_data = soup.find_all(True, {search_attr: search_key})
            elif (search_attr != None):
                if (search_attr.lower() == 'id'):
                    soup_data = soup.find(search_tag, {search_attr, search_key})
                else:
                    soup_data = soup.find_all(search_tag, {search_attr, search_key})
            else:
                soup_data = soup.find_all(search_tag)

            for i in soup_data:
                try:
                    if ("".join(i['class']).find("nc") >= 0):
                        pass
                    else:

                        find_a = i.find('a', {'class': 'sj_ln'})

                        img = "https://lh3.googleusercontent.com/Hc4D74YO7FYttrPCm5MuDm91NLblaaunJ6Y38WCg9mABUJfobgU_vXy1tjX668bI6xs=w300"
                        lock.acquire()
                        inven_data = {"web_site": "inven", "href": find_a['href'], "title": find_a.text, "img": img}
                        self.model.tb_detail_insert(query, inven_data)
                        lock.release()
                        print "insert"

                except Exception as e:
                    print e

        except Exception as e:
            print self.url_ + " "+ str(e)
            pass


## inven end ##

## 일베 start ##

class ilbe_find(threading.Thread):
    def __init__(self, board):
        threading.Thread.__init__(self)
        global query
        self.url = "https://www.ilbe.com/?mid=index&act=IS&where="+board+"&search_target=title_content&is_keyword="+query
        req_queue = Queue.Queue()
        header = {"user-agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36"}
        YPIMcrawler_nonlogin(req_queue, self.url, header, "div", "class", "pagination a1").start()  # class
        self.data = req_queue.get()
        #print self.data

    def run(self):
        db = model.model(conn)

        max_page = 0
        try:

            for i in self.data:
                max_page = len(i.findAll('a'))

            if ( max_page > 3):
                max_page = 3

            now_page = 1
            while( now_page <= max_page):
                ilbe_paging_find(db, self.url+"&page=", now_page).start()
                now_page += 1

        except Exception as e:
            print e

class ilbe_paging_find(threading.Thread):
    def __init__(self, db,url, page):
        threading.Thread.__init__(self)
        req_queue = Queue.Queue()
        header = {"user-agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36"}
        YPIMcrawler_nonlogin(req_queue, url+str(page), header, "ul", "class", "searchResult").start()  # class
        #print url+str(page)
        self.data = req_queue.get()
        self.db = db

    def run(self):
        global query, lock
        print "일베 run..."
        for i in self.data:
            for j in i.findAll('li'):
                try:

                    img = "ilbe.png"
                    ilbe_data = {"web_site":"ilbe","href":j.dl.dt.a['href'], "title":j.text,"img":img}
                    lock.acquire()
                    self.db.tb_detail_insert(query, ilbe_data)
                    lock.release()

                except:
                    pass

## 일베 end ##

## Bing start ##
def bing_find():
    global query
    url = "https://www.bing.com/search?&q=" + urllib.quote("\""+query+"\"")

    req_queue = Queue.Queue()
    header = {"user-agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36"}
    YPIMcrawler_nonlogin(req_queue, url, header, "span", "class", "sb_count").start()  # class
    data = req_queue.get()
    db = model.model(conn)

    max_page = 0
    try:

        for i in data:


            max_page = math.ceil(int(i.text.encode("utf-8").replace(',', "").replace('결과',"")) / 10.0)

            if (max_page > 7 ):
                max_page = 7
        now_page = 1
        first = 1
        while(now_page < max_page):
            bing_paging_find(db,url,first).start()
            first += 10
            now_page += 1

    except Exception as e:
        print e


class bing_paging_find(threading.Thread):
    def __init__(self, db,url, page):

        threading.Thread.__init__(self)
        req_queue = Queue.Queue()
        header = {"user-agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36"}
        YPIMcrawler_nonlogin(req_queue, url+"&first="+str(page), header, "li", "class", "b_algo").start()  # class
        #print url+str(page)
        self.data = req_queue.get()
        self.db = db

    def run(self):
        global query, lock
        print "bing run..."
        for i in self.data:
            try:
                img = "bing.jpg"
                bing_data = {"web_site":"bing","href":i.a['href'], "title":i.text,"img":img}
                lock.acquire()

                self.db.tb_detail_insert(query, bing_data)
                lock.release()

            except Exception as e:
                print e


## Bing end ##

## Yahoo start ##

def yahoo_find():
    global query
    url = "https://search.yahoo.com/search?fr=yfp-t&fp=1&toggle=1&cop=mss&ei=UTF-8&p=" + "\""+query+"\""

    req_queue = Queue.Queue()
    header = {"user-agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36"}
    YPIMcrawler_nonlogin(req_queue, url, header, "div", "class", "compPagination").start()  # class
    data = req_queue.get()
    db = model.model(conn)

    max_page = 0
    try:
        for i in data:

            max_page = math.ceil(int(i.span.text.replace(" results", "").replace(",","")) / 10.0)

            if (max_page > 7 ):
                max_page = 7
        now_page = 1
        first = 1
        while(now_page < max_page):

            yahoo_paging_find(db,url,first).start()
            first += 10
            now_page += 1

    except Exception as e:
        print e


class yahoo_paging_find(threading.Thread):
    def __init__(self, db,url, page):

        threading.Thread.__init__(self)
        req_queue = Queue.Queue()
        header = {"user-agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36"}
        YPIMcrawler_nonlogin(req_queue, url+"&b="+str(page), header, "div", "id", "main").start()  # class
        #print url+str(page)
        self.data = req_queue.get()
        self.db = db

    def run(self):
        global query, lock
        print "yahoo run..."
        for i in self.data:

                for j in i.findAll('li'):
                    try:
                        if (j['id']):

                            img = "yahoo.jpg"
                            yahoo_data = {"web_site":"yahoo","href":j.a['href'], "title":j.text,"img":img}
                            lock.acquire()
                            self.db.tb_detail_insert(query, yahoo_data)
                            lock.release()
                    except Exception as e:
                        pass




## Yahoo end ##

######################################################################

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
                request = urllib2.Request(url=self.url, headers=self.header)
                html = urllib2.urlopen(request)
            else:
                html = urllib2.urlopen(self.url)

            soup = BeautifulSoup(html.read(), "html.parser")

            if (self.search_tag == None):
                soup_data = [soup]
            elif (self.or_ == True):
                soup_data = soup.find_all(True, {self.search_attr:self.search_key})
            elif (self.search_attr != None):
                if (self.search_attr.lower() == 'id'):
                    soup_data = [soup.find(self.search_tag, {self.search_attr:self.search_key})]

                else:
                    soup_data = soup.find_all(self.search_tag, {self.search_attr:self.search_key})

            else:
                soup_data = soup.find_all(self.search_tag)

            self.queue.put(soup_data)
        except Exception as e:
            print e
            print self.url + " open error"
            pass
