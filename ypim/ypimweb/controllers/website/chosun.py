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
