# -*- coding: utf-8 -*-
from time import sleep
from scriptUtils import utils, excel
import threading
import xlsxwriter as wx
import matplotlib.pyplot as plt


class CpuData(threading.Thread):
    def __init__(self, pkg):
        super(CpuData, self).__init__()
        self.total_before = None
        self.total_after = None
        self.process_before = None
        self.process_after = None
        self.ls = []
        self.pkg = pkg

    # 获取APP的PID
    def get_pid(self):
        pid = utils.get_app_pid(self.pkg)
        return pid

    # 获取总CPU时间
    @staticmethod
    def get_total_cpu_time():
        time = utils.shell("cat /proc/stat|gawk '{print $2,$3,$4,$5,$6,$7,$8,$9,$10,$11}'").stdout.readline().split()
        total_time = 0
        for i in time:
            total_time += int(i)
        return total_time

    # 获取进程cpu时间
    def get_process_cpu_time(self):
        time = utils.shell(
            "cat /proc/%s/stat|gawk '{print $14,$15,$16,$17}'" % self.get_pid()).stdout.readline().split()
        pro_time = 0
        for i in time:
            pro_time += int(i)
        return pro_time

    # 计算cpu占用率
    def run(self):
        self.total_before = self.get_total_cpu_time()
        self.process_before = self.get_process_cpu_time()
        while True:
            if utils.stop != True:
                break
            y = []
            sleep(1)
            tm = utils.timestamp()
            self.total_after = self.get_total_cpu_time()
            self.process_after = self.get_process_cpu_time()
            usage = str(
                round(float(self.process_after - self.process_before) / float(self.total_after - self.total_before),
                      4) * 100)
            y.append(tm)
            y.append(usage)
            # print "CPU占用率：%s\n" % usage
            self.total_before = self.total_after
            self.process_before = self.process_after
            self.ls.append(y)

    def get_cpu(self):
        return self.ls


if __name__ == '__main__':
    cpu = CpuData("com.longtu.weifuhua")
    cpu.start()
    cpu.join()
