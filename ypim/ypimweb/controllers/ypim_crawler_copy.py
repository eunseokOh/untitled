# -*- encoding:utf-8 -*-

import multiprocessing as mp
from website import find_facebook, chosun_find, init, ddanzi_find, ppomppu_find, todayhumor_find
from ypim.ypimweb.models import db_conn, model

## crawler_pre
def ypim_crawler_facebook():
    print "facebook_run"
    find_facebook().start()

def ypim_crawler_chosun():
    board_list = ["news", "infomain", "photo", "movie", "community", "person", "qna"]
    print "chosun_run"
    for i in board_list:
        chosun_find(i).start()

def ypim_crawler_ddanzi():
    board_list = ["document", "comment"]  # ["content", "nick_name", "title"]
    print "ddanzi_run"
    for i in board_list:
        ddanzi_find(i).start()

def ypim_crawler_ppomppu():
    board_list = ["sub_memo"]  #["sub_memo","subject","csubject"]
    print "뽐뿌_run"
    for i in board_list:
        ppomppu_find(i).start()

        #todayhumor_find

def ypim_crawler_todayhumor():
    board_list = ["subject", "name"]  #["sub_memo","subject","csubject"]
    print "오유_run"
    for i in board_list:
        todayhumor_find(i).start()
### end


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

            crawler_class_list = [ypim_crawler_chosun, ypim_crawler_facebook, ypim_crawler_ppomppu, ypim_crawler_todayhumor] #ypim_crawler_ddanzi

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



