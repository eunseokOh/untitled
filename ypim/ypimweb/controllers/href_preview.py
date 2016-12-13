#-*- encoding:utf-8  -*-

from bs4 import BeautifulSoup
import urllib2, threading, Queue





"""
queue = Queue.Queue()
href = href_preview(queue,"http://www.naver.com")
href.start()
for i in queue.get():
    for j in i:
        print j+" = "+i[j]
"""