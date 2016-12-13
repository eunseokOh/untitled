import time


def count():
    num = 0
    sum = 0
    while(num < 30000000):
        num += 1
        sum += num
    print sum

start_time = time.time()
count()

print time.time() - start_time