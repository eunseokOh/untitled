#-*- encoding:utf-8 -*-

from flask import Flask, request, render_template, jsonify, redirect
from ypim_crawler import *
from ypim.ypimweb.models import model, db_conn
from url_vrius import Url_virus

conn = None
requestCount = -1

ypimweb = Flask(__name__, template_folder='../views')

@ypimweb.route("/search")
def hello():
    return render_template('hello.html')

@ypimweb.route("/urlvirus",methods=['POST'])
def urlvirus():
    url = request.get_data()
    return jsonify(Url_virus(url))

@ypimweb.route("/search/q=<query>/isfirst")
def isfirst(query):
    conn = db_conn.db_conn()
    model_ = model.model(conn)
    return jsonify(str(model_.tb_query_select(query.encode("utf-8"))[0]['que_seqno']))

@ypimweb.route("/search/groups/q=<query>")
def groups(query):
    conn = db_conn.db_conn()
    model_ = model.model(conn)
    return jsonify(model_.tb_detail_groups_cnt(query))

@ypimweb.route("/search/groups/q=<query>/w=<web_site>")
def web_site(query, web_site):
    conn = db_conn.db_conn()
    model_ = model.model(conn)
    print query, web_site
    return jsonify(model_.tb_detail_group(query, web_site))

@ypimweb.route("/search/q=<query>", methods=["GET","POST"])
def query(query):
    if (request.method == 'GET'):
        global requestCount
        requestCount += 1
        server_list = []
        server_list_cnt = requestCount % 5
        #server_list_cnt == 0
        if (True):
            return render_template('query.html', query=query)
        else:
            return redirect("http://www.naver.com")

    elif (request.method == 'POST'):
        req_Data = request.get_data()
        page_ = int(req_Data.replace("page=", ""))
        y_c = ypim_crawler(query, page_)
        crawler_list = y_c.run()
        print crawler_list

        return jsonify(crawler_list)

@ypimweb.route("/test")
def test():
    return render_template('test.html')

if __name__ == "__main__":
    ypimweb.run(host="localhost", debug=True)