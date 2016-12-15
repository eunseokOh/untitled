#-*- encoding:utf-8 -*-

from flask import Flask, request, render_template, jsonify
from ypim.ypimweb.models import db_conn
from ypim_crawler import *

conn = None

ypimweb = Flask(__name__, template_folder='../views')

@ypimweb.route("/search")
def hello():
    return render_template('hello.html')

@ypimweb.route("/search/q=<query>", methods=["GET","POST"])
def query(query):
    if (request.method == 'GET'):

        return render_template('query.html', query=query)
    elif (request.method == 'POST'):
        print "post go"
        crawler_list = ypim_crawler(query).run()

        return jsonify(crawler_list)


@ypimweb.route("/test")
def test():
    return render_template('test.html')

if __name__ == "__main__":


    ypimweb.run(host="192.168.21.69", debug=True)