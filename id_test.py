import time
import pp



def count():
    num = 0
    sum = 0
    while(num < 30000000):
        num += 1
        sum += num
    return sum



ppservers = tuple('*')
job_server = pp.Server(ppservers=ppservers)
start_time = time.time()
f1 = job_server.submit(count)
res = f1()

print res

print job_server.print_stats()

print time.time() - start_time
