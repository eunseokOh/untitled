#-*- encoding=utf-8 -*-
import MySQLdb as mysql



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

####################### tb_query #######################

    def tb_query_insert(self, query):
        sql  = """insert into tb_query(query)
                        values (%s)"""
        return self.mysql_query(sql, (query,))

    def tb_query_select(self, query):

        sql = """select max(que_seqno) as 'que_seqno'
                     from tb_query
                     where query = %s and
                     input_date >= date_add(NOW(), interval -3 hour) """

        return self.mysql_query(sql, (query,))
        #>= DATE_ADD(NOW(), INTERVAL -1 HOUR)

    def tb_query_delete(self):
        pass

    def tb_query_update(self):
        pass

####################### tb_detail #######################
    def tb_detail_groups_cnt(self, query):
        sql = """select web_site, count(web_site) as cnt
                      from tb_detail
                      where que_seqno = (select max(que_seqno) as 'que_seqno'
                                         from tb_query
                                         where query = %s and
                                         input_date >= date_add(NOW(), interval -3 hour))
                      group by web_site
                      """
        query = query.encode('UTF-8').decode('latin-1')
        data = self.mysql_query(sql, (query,))

        return data

    def tb_detail_group(self, query, web_site):
        sql = """select distinct href, det_seqno, que_seqno, title, img, web_site
                  from tb_detail
                  where que_seqno = (select max(que_seqno) as 'que_seqno'
                                     from tb_query
                                     where query = %s and
                                     input_date >= date_add(NOW(), interval -3 hour))
                        and web_site = %s
                         """
        query = query.encode('UTF-8').decode('latin-1')
        data = self.mysql_query(sql, (query,web_site))

        return data

    def tb_detail_count(self, query):

        sql = """select count(1) as cnt
                 from tb_detail
                 where que_seqno = (select max(que_seqno) from tb_query where query = %s)
                """
        return self.mysql_query(sql, (query,))

        pass
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
        sql = """select distinct href, det_seqno, que_seqno, title, img, web_site
                  from tb_detail
                  where que_seqno = %s """

        return self.mysql_query(sql, (que_seqno,))

    def tb_detail_select_page(self, que_seqno, page):
        page = (page-1)*60


        sql = """select distinct href, det_seqno, que_seqno, title, img, web_site
                  from tb_detail
                  where que_seqno = %s
                  ORDER BY title
                  LIMIT %s, 60"""

        return self.mysql_query(sql, (que_seqno, page))

    def tb_detail_delete(self, query):
        pass

    def tb_detail_update(self, query):
        pass

####################### tb_url #######################

    def tb_url_insert(self, web_site):
        sql = """insert into tb_url(web_site)
                 values(%s)"""

        return self.mysql_query(sql, (web_site,))

    def tb_url_select(self, web_site):
        sql = """select max(url_seqno) as url_seqno
                 from tb_url
                 where web_site = %s"""

        return self.mysql_query(sql, (web_site,))

    def tb_url_delete(self, query):
        pass

    def tb_url_update(self, query):
        pass

####################### tb_url_detail #######################

    def tb_url_detail_insert(self, url_seqno, part_num, href):
        sql =  """insert into tb_url_detail(url_seqno, part_num, href)
                  values(%s,%s,%s)"""

        return self.mysql_query(sql, (url_seqno, part_num, href.encode('UTF-8').decode('latin-1')))


    def tb_url_detail_select(self, web_site, part_num):

        sql = """select distinct href
                from tb_url_detail
                where url_seqno = (select max(url_seqno) from tb_url where web_site = %s)
                and part_num = %s """

        return self.mysql_query(sql, (web_site, part_num))

    def tb_url_detail_delete(self, query):
        pass

    def tb_url_detail_update(self, query):
        pass

