# -*- coding: utf-8 -*-
from time import sleep
from scriptUtils import utils
import threading


class CpuTempData(threading.Thread):
    def __init__(self):
        super(CpuTempData, self).__init__()
        self.ls = []

    def run(self):
        while True:
            if utils.stop!=True:
                break
            sleep(1)
            y = []
            tm = utils.timestamp()
            result = utils.shell("cat /sys/class/thermal/thermal_zone0/temp").stdout.readline()
            if "No such file or directory" in result:
                result = 0
            y.append(tm)
            y.append("".join(list(result)[0:2])+"."+"".join(list(result)[2:]))
            self.ls.append(y)

    def get_cpu_temp(self):
        return self.ls


if __name__ == '__main__':
    t = CpuTempData(3)
    t.start()
    t.join()