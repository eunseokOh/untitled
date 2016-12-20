#-*- encoding:utf-8 -*-
import MySQLdb as mysql
#21.115 학원
#35.213 house
host = "192.168.35.213"
user = "ypim"
db = "ypim_test"

#set foreign_key_checks = 0;
#truncate table

class db_conn():
    def db_conn(self):
        global host, user, db
        conn = mysql.connect(host=host, user=user, db=db)

        return conn