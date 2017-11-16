# -*- coding: utf-8 -*-
from scriptUtils import utils, excel
from time import sleep
import threading
import cProfile


class MemoryData(threading.Thread):
    def __init__(self, pkg):
        super(MemoryData, self).__init__()
        self.ls = []
        self.pkg = pkg

    def run(self):
        mem_command = "dumpsys meminfo %s|gawk '/MEMINFO/,/App Summary/'|grep TOTAL|gawk '{print $2,$3,$4,$5,$6,$7,$8}'" % self.pkg
        while True:
            if utils.stop != True:
                break
            sleep(1)
            y = []
            tm = utils.timestamp()
            results = utils.shell(mem_command).stdout.readline().split()
            # print "内存：%s" % results

            y.append(tm)
            for index in results:
                y.append(index)
            self.ls.append(y)

    def get_mem(self):
        return self.ls


if __name__ == '__main__':
    mem = MemoryData(1, "com.longtu.weifuhua")
    mem.start()
    mem.join()
