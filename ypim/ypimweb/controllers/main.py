#-*- encoding:utf-8 -*-

from flask import Flask, request, render_template, jsonify
from ypim_crawler import *
from ypim.ypimweb.models import model, db_conn

conn = None

ypimweb = Flask(__name__, template_folder='../views')

@ypimweb.route("/search")
def hello():
    return render_template('hello.html')

@ypimweb.route("/search/q=<query>/isfirst")
def isfirst(query):
    db_conn_ = db_conn.db_conn()
    conn = db_conn_.db_conn()
    model_ = model.model(conn)

    return jsonify(model_.tb_query_select(query.encode('UTF-8'))[0]['que_seqno'])

@ypimweb.route("/search/groups/q=<query>")
def groups(query):

    db_conn_ = db_conn.db_conn()
    conn = db_conn_.db_conn()
    model_ = model.model(conn)
    return jsonify(model_.tb_detail_groups_cnt(query))

@ypimweb.route("/search/groups/q=<query>/w=<web_site>")
def web_site(query, web_site):

    db_conn_ = db_conn.db_conn()
    conn = db_conn_.db_conn()
    model_ = model.model(conn)
    print query, web_site
    return jsonify(model_.tb_detail_group(query, web_site))



@ypimweb.route("/search/q=<query>", methods=["GET","POST"])
def query(query):
    if (request.method == 'GET'):
        return render_template('query.html', query=query)

    elif (request.method == 'POST'):
        req_Data = request.get_data()
        page_ = int(req_Data.replace("page=",""))

        y_c = ypim_crawler(query, page_)
        crawler_list = y_c.run()
        print crawler_list

        return jsonify(crawler_list)


@ypimweb.route("/test")
def test():
    return render_template('test.html')

if __name__ == "__main__":
    ypimweb.run(host="localhost", debug=True)