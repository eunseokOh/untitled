#-*- encoding=utf-8 -*-
import MySQLdb as mysql



class model():
    def __init__(self,conn_):
        self.conn = conn_

    def mysql_query(self, sql, values = None):

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

####################### tb_query #######################

    def tb_query_insert(self, query):
        sql  = """insert into tb_query(query)
                        values (%s)"""
        return self.mysql_query(sql, (query,))

    def tb_query_select(self, query):
        sql = """select max(que_seqno) as 'que_seqno'
                     from tb_query
                     where query = %s and
                     input_date >= date_add(NOW(), interval -1 hour) """

        return self.mysql_query(sql, (query,))
        #>= DATE_ADD(NOW(), INTERVAL -1 HOUR)

    def tb_query_delete(self):
        pass

    def tb_query_update(self):
        pass

####################### tb_detail #######################

    def tb_detail_insert(self, query, data):

        que_seqno = self.tb_query_select(query)[0]['que_seqno']
        #print que_seqno
        try:
            web_site = data['web_site'].encode('UTF-8').decode('latin-1')
            href = data['href'].encode('UTF-8').decode('latin-1')
            title = data['title'].encode('UTF-8').decode('latin-1')
            img = data['img']

            if(img != None):
                img = data['img'].encode('UTF-8').decode('latin-1')

        except Exception as e:
            print e


        finally:
            sql = """insert into tb_detail(que_seqno, web_site, href, title, img)
                               values (%s, %s, %s, %s, %s)"""
        return self.mysql_query(sql, (que_seqno, web_site, href, title, img))

    def tb_detail_select(self, que_seqno):
        sql = """select *
                 from tb_detail
                 where que_seqno = %s """

        return self.mysql_query(sql, (que_seqno,))

    def tb_detail_delete(self, query):
        pass

    def tb_detail_update(self, query):
        pass
