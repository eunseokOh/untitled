#-*- encoding:utf-8 -*-
import MySQLdb as mysql
#21.115 학원
#35.213 house
#set foreign_key_checks = 0;
#truncate table

def db_conn():
    host = "192.168.21.115"
    user = "ypim"
    db = "ypim_test"
    conn = mysql.connect(host=host, user=user, db=db)

    return conn