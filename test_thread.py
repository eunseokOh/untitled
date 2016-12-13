import threading
import urllib2, Queue, time, multiprocessing as mp

class hello3(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.queue = queue

    def run(self):
        global start_time
        html = urllib2.urlopen("http://www.google.co.kr")
        #print html
        end_time = time.time()
        print end_time-start_time

class hello2(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.queue = queue

    def run(self, ):
        html = urllib2.urlopen("http://www.google.co.kr")
       # print html

        for i in range(5):
            hello3().start()

class hello(threading.Thread):
    def __init__(self, queue):
        mp.Process.__init__(self)
        self.queue = queue

    def run(self):
        html = urllib2.urlopen("http://www.google.co.kr")
        self.queue.put(html)
        for i in range(5):
            hello2().start()

start_time = time.time()
for i in range(5):
    queue = Queue.Queue()
    hello(queue).start()
    print queue.get()



