#-*- encoding:utf-8 -*-
import MySQLdb as mysql
#21.115 학원
#35.213 house
host = "192.168.21.115"
user = "ypim"
db = "ypim_test"

class db_conn():
    def db_conn(self):
        global host, user, db
        conn = mysql.connect(host=host, user=user, db=db)

        return conn

class model():
    def __init__(self,conn_):
        self.conn = conn_

    def mysql_query(self, sql, values = None):
        #print sql
        #print values
        results = None

        if (sql.find('select') >= 0):
            cursor = self.conn.cursor(cursorclass=mysql.cursors.DictCursor)
        else:
            cursor = self.conn.cursor()
            #print values
        try:
            if (values != None):
                cursor.execute(sql, values)
            else:
                cursor.execute(sql)
            self.conn.commit()
            results = cursor.fetchall()

        except Exception as e:
            print e
            self.conn.rollback()
            results = "error"

        finally:

            return results

def query_test():
    db_conn_ = db_conn()
    conn = db_conn_.db_conn()
    model_ = model(conn)


    sql  = """select * from tb_detail where que_seqno = 140 and web_site = %s
              """
    sql2 =  """select *
              from tb_detail
              where que_seqno = (select max(que_seqno) as 'que_seqno'
                                 from tb_query
                                 where query = %s and
                                 input_date >= date_add(NOW(), interval -72 hour))
              """
    return model_.mysql_query(sql2, ('lady',))

for i in query_test():
    print i