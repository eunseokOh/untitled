import multiprocessing as mp
import urllib2, Queue, time, threading
start_time = time.time()

def hello3():


    global start_time
    html = urllib2.urlopen("http://www.google.co.kr")
    #print html
    print time.time()


def hello2():

    html = urllib2.urlopen("http://www.google.co.kr")
    #print html
    for i in range(5):
        p = mp.Process(target=hello3)
        p.start()

def hello():

    html = urllib2.urlopen("http://www.google.co.kr")
    print "!"
    for i in range(5):
        p = mp.Process(target=hello2)
        p.start()

if __name__ == '__main__':
    mp.freeze_support()

    for i in range(5):
        p = mp.Process(target=hello)
        p.start()



