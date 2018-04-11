#!/usr/bin/env python
# -*- coding: utf-8 -*-

import Tkinter as tk
import os
import shutil
import platform
import re
import subprocess
import time
import ttk
from  exception import SriptException
stop = True
runNum = None

#判断系统类型，windows使用findstr，linux使用grep
system = platform.system()
if system is "Windows":
    find_util = "findstr"
else:
    find_util = "grep"

#判断是否设置环境变量ANDROID_HOME
if "ANDROID_HOME" in os.environ:
    if system == "Windows":
        command = os.path.join(os.environ["ANDROID_HOME"], "platform-tools", "adb.exe")
    else:
        command = os.path.join(os.environ["ANDROID_HOME"], "platform-tools", "adb")
else:
    raise EnvironmentError(
        "Adb not found in $ANDROID_HOME path: %s." %os.environ["ANDROID_HOME"])


def get_screen_size(window):
    return window.winfo_screenwidth(),window.winfo_screenheight()

def get_window_size(window):
    return window.winfo_reqwidth(),window.winfo_reqheight()

def center_window(root, width, height):
    screenwidth = root.winfo_screenwidth()
    screenheight = root.winfo_screenheight()
    size = '%dx%d+%d+%d' % (width, height, (screenwidth - width)/2, (screenheight - height)/2)
    root.geometry(size)

class Window(object):
    device_id = ""
    device_id_list = []
    root = None
    box = None
    def __init__(self, device_id_list, root):
        self.device_id_list = device_id_list
        self.device_id = device_id_list[0]
        self.root = root
        self.box = None

    def show_window(self):
        self.root.title(u'Serialno Number')
        center_window(self.root, 300, 240)
        self.root.maxsize(600, 400)
        self.root.minsize(300, 240)

        options = self.device_id_list
        self.box = ttk.Combobox(values=options)
        self.box.current(0)
        self.box.pack(expand = tk.YES)
        self.box.bind("<<ComboboxSelected>>", self.select)
        ttk.Button(text=u"确定", command=self.ok).pack(expand = tk.YES)

        self.root.mainloop()


    def select(self, event=None):
        self.device_id = self.box.selection_get()

    def ok(self):
        global serialno_num
        serialno_num = self.device_id
        self.root.destroy()

# adb命令
def adb(args):
    global serialno_num
    if serialno_num == "":
        devices = get_device_list()
        if len(devices) == 1:
            #global serialno_num
            serialno_num = devices[0]
        else:
            root = tk.Tk()
            window = Window(devices, root)
            window.show_window()
    cmd = "%s -s %s %s" %(command, serialno_num, str(args))
    return subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

#adb shell命令
def shell(args):
    global serialno_num
    if serialno_num == "":
        devices = get_device_list()
        if len(devices) == 1:
            serialno_num = devices[0]
        else:
            root = tk.Tk()
            window = Window(devices, root)
            window.show_window()
    cmd = "%s -s %s shell %s" %(command, serialno_num, str(args))
    return subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

#获取设备状态
def get_state():
    return os.popen("adb -s %s get-state" % serialno_num).read().strip()

#获取对应包名的pid
def get_app_pid(pkg_name):
    if system is "Windows":
        string = shell("ps | findstr %s$" %pkg_name).stdout.read()

    string = shell("ps | grep -w %s" %pkg_name).stdout.read()

    if string == '':
        return "the process doesn't exist."

    pattern = re.compile(r"\d+")
    result = string.split(" ")
    result.remove(result[0])

    return  pattern.findall(" ".join(result))[0]

#杀掉对应包名的进程
def kill_process(pkg_name):
    pid = get_app_pid(pkg_name)
    result = shell("kill %s" %str(pid)).stdout.read().split(": ")[-1]
    if result != "":
        raise SriptException("Operation not permitted or No such process or Permission denied")


# 杀掉应用程序
def kill_application(pkg_name):
    shell("am force-stop %s" % pkg_name)


#获取设备上当前应用的包名与activity
def get_focused_package_and_activity():
    #pattern = re.compile(r"[a-zA-Z0-9\.]+/.[a-zA-Z0-9\.]+")
    #out = shell("dumpsys window w | %s \/ | %s name=" %(find_util, find_util)).stdout.read()

    #return pattern.findall(out)[0]
    return shell("dumpsys activity activities | findstr mFocusedActivity").stdout.read().split()[-1][:-1]

#获取当前应用的包名
def get_current_package_name():
    return get_focused_package_and_activity().split("/")[0]

#获取当前设备的activity
def get_current_activity():
    return get_focused_package_and_activity().split("/")[-1]

#时间戳
def timestamp():
    return time.strftime('%Y-%m-%d-%H-%M-%S',time.localtime(time.time()))

def get_device_list():
    devices = []
    result = subprocess.Popen("adb devices", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout.readlines()
    result.reverse()
    for line in result[1:]:
        if "attached" not in line.strip():
            devices.append(line.split()[0])
        else:
            break
    return devices


# 获取设备名称
def get_device_name():
    brandName = shell("cat /system/build.prop | findstr ro.product.brand").stdout.readline().split("=")[1].strip()
    deviceName = shell("cat /system/build.prop | findstr ro.product.model").stdout.readline().split("=")[1].strip()
    result = "{brand}_{device}".format(brand=brandName, device=deviceName)
    return result
# 检查设备状态
if get_state() != "device":
    adb("kill-server").wait()
    adb("start-server").wait()

if get_state() != "device":
    raise SriptException("Device not run")

# 获取设备序列号
def get_serialno():
    return adb("get-serialno").stdout.readline()


# 获取APP的uid
def get_app_uid(pkg_name):
    pid = get_app_pid(pkg_name)
    uid = shell("cat /proc/%s/status|findstr Uid" % pid).stdout.readline().split()[1]
    return uid


# 获取CPU型号
def get_cpu_model():
    return shell("cat /proc/cpuinfo|findstr Hardware").stdout.readline().strip().split(":")[1]


# 获取设备总内存
def get_total_memory():
    result = shell('cat /proc/meminfo|findstr "MemTotal"').stdout.readline().split(":")[1].strip()
    MemTotal = "{val}MB".format(val=int(result.split()[0]) / 1024)
    return MemTotal


# 获取设备分辨率
def get_DisplayDeviceInfo():
    result = shell("dumpsys display | findstr DisplayDeviceInfo").stdout.readline().split(",")[1].strip()
    return result


# 获取系统版本号
def get_system_version():
    return shell("cat /system/build.prop | findstr ro.build.version.release").stdout.readline().split("=")[1]


# 获取SDK版本号
def get_sdk_version():
    return shell("cat /system/build.prop | findstr ro.build.version.sdk").stdout.readline().split("=")[1]


# 获取设备CPU最大频率
def get_cpu_max_frequency():
    max_frequency = shell("su -c 'cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_max_freq'").stdout.readline().strip()
    if "not found" in max_frequency:
        max_frequency = "Permission denied"
        return max_frequency
    else:
        return "{val}MHz".format(val=int(max_frequency) / 1000)


# 获取设备CPU最小频率
def get_cpu_min_frequency():
    min_frequency = shell("cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_min_freq").stdout.readline().strip()
    return "{val}MHz".format(val=int(min_frequency) / 1000)

# 截图保存至sd卡adbscreenshot目录并同步电脑
def screenshot():
    if "directory" in shell("ls /sdcard/adbScreenShot").stdout.readline():
        shell("mkdir /sdcard/adbScreenShot")
    shell("/system/bin/screencap -p /sdcard/adbScreenShot/%s.png" % timestamp()).wait()
    if os.path.exists("D://adbScreenShot"):
        shutil.rmtree("D://adbScreenShot")
    adb("pull /sdcard/adbscreenshot D://adbScreenShot")



if __name__ == "__main__":
    pass
