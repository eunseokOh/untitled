import MySQLdb as mysql

host = "192.168.21.115"
user = "ypim"
db = "ypim_test"

class db_conn():
    def db_conn(self):
        global host, user, db
        conn = mysql.connect(host=host, user=user, db=db)

        return conn