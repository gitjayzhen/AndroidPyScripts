# coding=utf-8
import threading
import re
import json
from scriptUtils import utils


class DeviceInfo(threading.Thread):
    def __init__(self):
        super(DeviceInfo, self).__init__()

    def get_cpuModel(self):
        print "CPU型号：", utils.shell("cat /proc/cpuinfo|findstr Hardware").stdout.readline().strip().split(":")[1]

    def get_memInfo(self):
        result = utils.shell('cat /proc/meminfo|findstr "MemTotal"').stdout.readline().split(":")[1].strip()
        MemTotal = "{val}MB".format(val=int(result.split()[0])/1024)
        print "总内存：%s" % MemTotal

    def get_DisplayDeviceInfo(self):
        result = utils.shell("dumpsys display | findstr DisplayDeviceInfo").stdout.readline().split(",")[1].strip()
        print "分辨率：", result

    def get_deviceBrand(self):
        # print "厂商：", utils.shell("cat /system/build.prop | findstr ro.product.brand").stdout.readline().split("=")[1], utils.get_device_name()
        print utils.get_device_name()

    def get_systemVersion(self):
        print "系统版本：", utils.shell("cat /system/build.prop | findstr ro.build.version.release").stdout.readline().split("=")[1]

    def get_sdkVersion(self):
        print "SDK版本：", utils.shell("cat /system/build.prop | findstr ro.build.version.sdk").stdout.readline().split("=")[1]

    def get_cpuFrequency(self):
        print utils.get_cpu_max_frequency()
        print utils.get_cpu_min_frequency()

if __name__ == '__main__':
    info = DeviceInfo()
    info.start()
    info.get_cpuModel()
    info.get_memInfo()
    info.get_DisplayDeviceInfo()
    info.get_deviceBrand()
    info.get_systemVersion()
    info.get_sdkVersion()
    info.get_cpuFrequency()
    info.join()
