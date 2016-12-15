import multiprocessing as mp

def init(query_):
    global query
    query = query_


def hello():
    global query
    print query + "11"

def run():
    pool=mp.Pool(initializer=init, initargs=("hello",))
    for i in range(5):
        p = pool.apply_async(hello)
        p.get()

run()


