# -*- encoding:utf-8 -*-

from bs4 import BeautifulSoup
import mechanize, urllib2, threading, Queue, math, time
import multiprocessing as mp

query = "010-9523-0324".encode("utf-8")


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
    def __init__(self, req_queue):
        threading.Thread.__init__(self)
        # req_class, url, header, search_tag, search_attr, search_key, id_tag, pass_tag, id_, pass_
        self.url = 'http://www.facebook.com/login.php'
        self.header = [('user-agent',
                        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36')]
        self.id_ = "experiment9090@gmail.com"
        self.pass_ = "ypim9090"
        queue = Queue.Queue()
        self.req_queue = req_queue

        # self, queue, url, header, search_tag, search_attr, search_key, id_tag, pass_tag, id_, pass_
        YPIMcrawler_login(queue, self.url, self.header, None, None, None, 'email', 'pass', self.id_, self.pass_).start()

        self.broswer = queue.get()

    def run(self):
        global query
        #print query
        url = "https://www.facebook.com/search/str/" + query + "/keywords_users"
        resp = self.broswer.open(url)  # data = set_cookie_broswer (cookie 값 저장됨)
        html = str(resp.read()).replace("<!--", "").replace("-->", "")
        Soup = BeautifulSoup(html, "html.parser")

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


            face_data = {"href": each_url, "title": title}

            return_facebook_list.append(face_data)
        self.req_queue.put(return_facebook_list)
        print "facebook_end"


## end facebook ##

## 조선 일보 ##
class chosun_find(threading.Thread):
    def __init__(self, return_queue, board):
        threading.Thread.__init__(self)
        global query
        self.url = "http://search.chosun.com/search/" + board + ".search?query=" + query + "&pageno="
        #
        # self.page = str(page)
        self.return_queue = return_queue
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

                while (True):
                    if (now_page > total_page_no):
                        break
                    else:
                        print "chosun_find_threading..."
                        queue = Queue.Queue()

                        chosun_paging_find(queue, self.url, now_page).start()

                        for i in queue.get():
                            href = i['href']
                            title = i['title']
                            return_list.append({'title':title,'href':href})
                        #print "/".join(queue.get())
                        #return_list.append(  )
                    now_page += 1
                    end_page_no += 1

                    if (end_page_no == 11):
                        end_page_no = total_page_no
                        break

            except:
                print "chosun Error"
                pass
        self.return_queue.put(return_list)


class chosun_paging_find(threading.Thread):
    def __init__(self, queue, url, page):
        threading.Thread.__init__(self)
        req_queue = Queue.Queue()
        YPIMcrawler_nonlogin(req_queue, url + str(page), None, "div", "class", "result_box").start()  # class
        self.data = req_queue.get()
        self.queue = queue

    def run(self):
        return_list = []

        for i in self.data:
            for j in i.section.findAll('dt'):  # title + href

                return_list.append({'title': j.text, 'href': j.a['href']})

                # print j.text + " = "+ j.a['href']

        self.queue.put(return_list)


## 조선 일보 END ##

## crawler_pre
def ypim_crawler_facebook():

    print "facebook_run"
    return_list = []
    queue = Queue.Queue()

    find_facebook(queue).start()
    fd_list = queue.get()
    if fd_list:
        return_list.append({"facebook": fd_list})
    else:
        return_list = None

    print return_list


def ypim_crawler_chosun():

    return_list = []
    board_list = ["news", "infomain", "photo", "movie", "community", "person", "qna"]
    chosun_list = []
    print "chosun_run"
    for i in board_list:
        try:
            queue = Queue.Queue()
            chosun_find(queue, i).start()
            for i in queue.get():
                if i:
                    return_list.append(i)

        except:
            pass


    #return_list.append({"chosun": queue.get()})

    chosun_list.append({"chosun":return_list})
    print chosun_list
### end


def ypim_crawler():
    crawler_class_list = [ypim_crawler_facebook, ypim_crawler_chosun]
    manager = mp.Manager()
    return_dic = manager.dict()

    for num, i in enumerate(crawler_class_list):
        mp.Process(target=i).start()





# pool = mp.Pool(processes=4)
    #result = pool.map_async(ypim_crawler_facebook, [None])
    #result = pool.map_async(ypim_crawler_chosun, [None])
    #result.wait()

if __name__ == "__main__":

    ypim_crawler()
