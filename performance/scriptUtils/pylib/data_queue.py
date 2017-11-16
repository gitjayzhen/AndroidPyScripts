#coding:utf-8
__author__ = 'yungenhui'


import threading
import Queue
import random
import time


def randomnum():
    while 1:
        time.sleep(2)
        print random.randint(1, 100)

thrend_q = Queue.Queue()
thrend_r = threading.Thread(target=randomnum)
thrend_r.start()
a = thrend_q.get()
print type(a)


