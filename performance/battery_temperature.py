# -*- coding: utf-8 -*-
from time import sleep
from utils import androiddebug
import threading


class BatteryTempData(threading.Thread):

    def __init__(self):
        super(BatteryTempData, self).__init__()
        self.ls = []

    def run(self):
        while True:
            if androiddebug.stop != True:
                break
            sleep(1)
            y = []
            dictionaries = {}
            tm = androiddebug.timestamp()
            # 这个温度单位是：
            result = androiddebug.shell("dumpsys battery").stdout.readlines()
            for i in result[1:]:
                new = i.split(":")
                dictionaries[new[0].strip()] = new[1].strip()
            y.append(tm)
            y.append("".join(list(dictionaries["temperature"])[0:2])+"."+"".join(list(dictionaries["temperature"])[2:]))
            self.ls.append(y)

    def get_battery_temp(self):
        return self.ls


if __name__ == '__main__':
    t = BatteryTempData()
    t.start()
    print t.get_battery_temp()
    t.join()

