# -*- encoding:utf-8 -*-

import multiprocessing as mp, math
from website import find_facebook, chosun_find, init, ddanzi_find, ppomppu_find, todayhumor_find, inven_find, ilbe_find, mlbpark_find, dcinside_find, clien_find
from ypim.ypimweb.models import db_conn, model

conn_ = None

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

def ypim_crawler_ilbe():
    board_list = ["document", "comment"]   #["sub_memo","subject","csubject"]
    print "일베_run"
    for i in board_list:
        ilbe_find(i).start()

def ypim_crawler_inven1():
    db = db_conn.db_conn()
    conn = db.db_conn()

    model_ = model.model(conn)
    return_list = model_.tb_url_detail_select("inven", 1)
    url_list = []
    for i in return_list:
        url_list.append(i['href'])

    name_list = ["subjcont", "nicname"]

    for i in name_list:
        for j in url_list:
            inven_find(model_, j, i).start()

def ypim_crawler_inven2():
    db = db_conn.db_conn()
    conn = db.db_conn()

    model_ = model.model(conn)
    return_list = model_.tb_url_detail_select("inven", 2)

    #url_list = ["http://www.inven.co.kr/board/powerbbs.php?come_idx=2730"]
    url_list = []
    for i in return_list:
        url_list.append(i['href'])

    name_list = ["subjcont", "nicname"]

    for i in name_list:
        for j in url_list:
            inven_find(model_,j, i).start()

def ypim_crawler_inven3():
    db = db_conn.db_conn()
    conn = db.db_conn()

    model_ = model.model(conn)
    return_list = model_.tb_url_detail_select("inven", 3)
    url_list = []
    for i in return_list:
        url_list.append(i['href'])

    name_list = ["subjcont", "nicname"]

    for i in name_list:
        for j in url_list:
            inven_find(model_, j, i).start()


def ypim_crawler_inven4():
    db = db_conn.db_conn()
    conn = db.db_conn()

    model_ = model.model(conn)
    return_list = model_.tb_url_detail_select("inven", 4)
    url_list = []
    for i in return_list:
        url_list.append(i['href'])

    name_list = ["subjcont", "nicname"]

    for i in name_list:
        for j in url_list:
            inven_find(model_, j, i).start()

def ypim_crawler_inven5():
    db = db_conn.db_conn()
    conn = db.db_conn()

    model_ = model.model(conn)
    return_list = model_.tb_url_detail_select("inven", 5)

    url_list = []
    for i in return_list:
        url_list.append(i['href'])

    name_list = ["subjcont","nicname"]

    for i in name_list:
        for j in url_list:
            inven_find(model_, j, i).start()

def ypim_crawler_inven6():
    db = db_conn.db_conn()
    conn = db.db_conn()

    model_ = model.model(conn)
    return_list = model_.tb_url_detail_select("inven", 6)

    url_list = []
    for i in return_list:
        url_list.append(i['href'])

    name_list = ["subjcont", "nicname"]

    for i in name_list:
        for j in url_list:
            inven_find(model_, j, i).start()

def ypim_crawler_inven7():
    db = db_conn.db_conn()
    conn = db.db_conn()

    model_ = model.model(conn)
    return_list = model_.tb_url_detail_select("inven", 7)

    url_list = []
    for i in return_list:
        url_list.append(i['href'])

    name_list = ["subjcont", "nicname"]

    for i in name_list:
        for j in url_list:
            inven_find(model_, j, i).start()

def ypim_crawler_inven8():
    db = db_conn.db_conn()
    conn = db.db_conn()

    model_ = model.model(conn)
    return_list = model_.tb_url_detail_select("inven", 8)

    url_list = []
    for i in return_list:
        url_list.append(i['href'])

    name_list = ["subjcont", "nicname"]

    for i in name_list:
        for j in url_list:
            inven_find(model_, j, i).start()

def ypim_crawler_inven9():
    db = db_conn.db_conn()
    conn = db.db_conn()

    model_ = model.model(conn)
    return_list = model_.tb_url_detail_select("inven", 9)

    url_list = []
    for i in return_list:
        url_list.append(i['href'])

    name_list = ["subjcont", "nicname"]

    for i in name_list:
        for j in url_list:
            inven_find(model_, j, i).start()

def ypim_crawler_inven10():
    db = db_conn.db_conn()
    conn = db.db_conn()

    model_ = model.model(conn)
    return_list = model_.tb_url_detail_select("inven", 10)

    url_list = []
    for i in return_list:
        url_list.append(i['href'])

    name_list = ["subjcont", "nicname"]

    for i in name_list:
        for j in url_list:
            inven_find(model_, j, i).start()

def ypim_crawler_inven11():
    db = db_conn.db_conn()
    conn = db.db_conn()

    model_ = model.model(conn)
    return_list = model_.tb_url_detail_select("inven", 11)

    url_list = []
    for i in return_list:
        url_list.append(i['href'])

    name_list = ["subjcont", "nicname"]

    for i in name_list:
        for j in url_list:
            inven_find(model_, j, i).start()

def ypim_crawler_inven12():
    db = db_conn.db_conn()
    conn = db.db_conn()

    model_ = model.model(conn)
    return_list = model_.tb_url_detail_select("inven", 12)

    url_list = []
    for i in return_list:
        url_list.append(i['href'])

    name_list = ["subjcont", "nicname"]

    for i in name_list:
        for j in url_list:
            inven_find(model_, j, i).start()

def ypim_crawler_clien():
    board_list = ["="]  # [=] 전체보기
    print "클리앙_run"
    for i in board_list:
        clien_find(i).start()

def ypim_crawler_dcinside():
    board_list = ['post']
    print "디시인사이드_run"
    for i in board_list:
        dcinside_find(i).start()

def ypim_crawler_mlbpark():
    board_list = ["bullpen2"]  # ["bullpen2"]
    print "엠팍_run"
    for i in board_list:
        mlbpark_find(i).start()


### end


class ypim_crawler():
    def __init__(self, query_, page):
        self.page = page
        self.query = query_.encode("utf-8")
        db = db_conn.db_conn()
        self.conn= db.db_conn()
        self.db = model.model(self.conn)
        self.cnt = self.db.tb_detail_count(self.query)


    def run(self):

        seq_que = self.db.tb_query_select(self.query)[0]['que_seqno']

        if(seq_que == None):

            self.db.tb_query_insert(self.query)
            crawler_class_list = [ypim_crawler_mlbpark, ypim_crawler_dcinside, ypim_crawler_clien,ypim_crawler_ilbe, ypim_crawler_chosun, ypim_crawler_facebook, ypim_crawler_ppomppu, ypim_crawler_todayhumor, ypim_crawler_inven1, ypim_crawler_inven2, ypim_crawler_inven3, ypim_crawler_inven4, ypim_crawler_inven5, ypim_crawler_inven6, ypim_crawler_inven7, ypim_crawler_inven8, ypim_crawler_inven9, ypim_crawler_inven10, ypim_crawler_inven11, ypim_crawler_inven12]#[ypim_crawler_ilbe, ypim_crawler_chosun, ypim_crawler_facebook, ypim_crawler_ppomppu, ypim_crawler_todayhumor]  #ypim_crawler_ddanzi

            try:
                pool = mp.Pool(initializer=init, initargs=(self.query,))
                for i in crawler_class_list:
                    p = pool.apply_async(i)
                    p.get()

            except Exception as e:
                print e

            finally:
                self.conn.close()

        else:
            query_dict = self.db.tb_detail_select_page(seq_que, self.page)
            try:

                max_page = math.ceil(self.cnt[0]['cnt'] / 60.0)
                query_dict[0].update({"max_page":max_page})
                return query_dict

            except Exception as e:
                print e
                return query_dict
            finally:
                self.conn.close()

if __name__ == '__main__':
    mp.freeze_support()

    # return return_list



