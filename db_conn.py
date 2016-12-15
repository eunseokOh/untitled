#-*- encoding=utf-8 -*-

import MySQLdb as mysql

host = "192.168.21.74"
user = "ypim"
db = "ypim_test"


def db_conn(sql, values = None):
    global host, user, db
    conn = mysql.connect(host=host, user=user, db=db)

    if (sql.find("insert") >= 0):
        cursor = conn.cursor(cursorclass=mysql.cursors.DictCursor)
    else:
        cursor = conn.cursor()

    try:
        if (values != None):
            cursor.execute(sql, values)
        else:
            cursor.execute(sql)
        conn.commit()
        results = cursor.fetchall()

    except Exception as e:
        print e
        conn.rollback()
        results = "error"

    finally:
        conn.close()
        return results



class tb_query():

    def insert(self, query):
        sql  = """insert into tb_query(query)
                    values (%s)"""
        return db_conn(sql, (query,))

    def select(self, query):
        sql = """select max(que_seqno)
                 from tb_query
                 where query = %s and
                 input_date >= date_add(NOW(), interval -3 hour) """

        return db_conn(sql, (query,))
        #>= DATE_ADD(NOW(), INTERVAL -1 HOUR)

    def delete(self):
        pass

    def update(self):
        pass


class tb_detail():
    def __init__(self):
        pass

    def insert(self, query=None, data=None):
        t_query = tb_query()
        que_seqno = t_query.select(query)


        sql = """insert into tb_detail(que_seqno, site, href, title, img)
                       values (%s, %s, %s, %s)"""
        return db_conn(sql, (que_seqno, "hello", "good", "bye"))

    def select(self, query):
        pass
        # >= DATE_ADD(NOW(), INTERVAL -1 HOUR)

    def delete(self, query):
        pass

    def update(self, query):
        pass



if __name__ == "__main__":
    t_detail = tb_detail()
    print t_detail.insert()

