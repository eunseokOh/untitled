#-*- encoding:utf-8 -*-
from bs4 import BeautifulSoup
import urllib2, threading, Queue
from ypim.ypimweb.models import model, db_conn



query = "은석"
list = []

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
                soup_data = soup.find(self.search_tag, {self.search_attr, self.search_key})
            else:
                soup_data = soup.find_all(self.search_tag, {self.search_attr, self.search_key})
        else:
            soup_data = soup.find_all(self.search_tag)
        if (self.queue != None):
            self.queue.put(soup_data)
        else:
            list = []
            if soup_data:
                for i in soup_data:
                    for j in i.findAll('a'):
                        if ( j['href'].find('http')>=0):

                            list.append(j['href'])

            self.queue.put(list)




#queue, url, header, search_tag, search_attr, search_key, or_=False
def inven():
    queue = Queue.Queue()
    url = "http://www.inven.co.kr/webzine/"
    YPIMcrawler_nonlogin(queue, url, None, "div", "class", "w150M").start()

    return queue.get()

##queue, url, header, search_tag, search_attr, search_key, or_=False
def inven_get_come_idx():
    list = []
    non_overlap_list = []
    """
    url = ["http://lovelive.inven.co.kr", "http://durango.inven.co.kr/"]

    for i in url:
        queue = Queue.Queue()
        t = YPIMcrawler_nonlogin(queue,  i, None, "li", "class", "firstMenuItem")
        t.start()
        list.append(queue.get())
    """
    try:

        for i in inven():
            for j in i.findAll('a'):
                queue = Queue.Queue()
                print j['href']
                t = YPIMcrawler_nonlogin(queue, j['href'], None, "li", "class", "firstMenuItem")
                t.start()
                list.append(queue.get())


        for i in list:
            for j in i:
                for x in j.parent:
                    try:
                        if(x.a['href'].find("come_idx") >= 0):
                            if (x.a['href'].find("category") >= 0):
                                non_overlap_list.append(x.a['href'])
                            else:
                                index = x.a['href'].find("come_idx")
                                try:
                                    href = int(x.a['href'][index+9:index + 13])

                                    non_overlap_list.append("http://www.inven.co.kr/board/powerbbs.php?come_idx="+str(href))
                                except Exception as e:
                                    print e
                                    pass
                    except:
                        pass
        db = db_conn.db_conn()
        conn = db.db_conn()

        model_ = model.model(conn)

        model_.tb_url_insert("inven")
        url_seqno = model_.tb_url_select("inven")[0]['url_seqno']

        part_num = 0
        lock = threading.Lock()
        for n, i in enumerate(set(non_overlap_list)):
            if (n % 100 == 0):
                part_num += 1

            lock.acquire()
            model_.tb_url_detail_insert(url_seqno, part_num, i)
            lock.release()

    except Exception as e:
        print e


if __name__ == "__main__":
    inven_get_come_idx()