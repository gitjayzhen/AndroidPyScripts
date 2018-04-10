# -*- coding: utf-8 -*-
from performance.scriptUtils import utils

#global udid, pkg
udid = "05e30052004512a8"
pkg = "com.longtu.weifuhua"


# 获取APP的UID
def uid():
    uid = ''
    return uid

# 获取APP的PID
def pid():
    pid = ''
    return pid


# 获取APP的CPU使用率
def cpu():
    cpu = "dumpsys cpuinfo|grep " + pkg + "|gawk '{print $1,$3,$6}'|sed 's/%//g'"
    return cpu


# 获取APP的内存使用率
def mem():
    mem = "dumpsys meminfo " + pkg + "|gawk '/MEMINFO/,/App Summary/'|grep TOTAL|gawk '{print $2,$3,$4,$5,$6,$7,$8}'"
    return mem


# 获取APP的GFX数据
def gfx():
    gfx = "dumpsys gfxinfo " + utils.get_focused_package_and_activity() + "|gawk '/Execute/,/Stats/'|gawk NF'{print $1,$2,$3,$4}'|grep -v '^Draw'|grep -v '^Stats'|sed '$d'"
    return gfx


# 获取APP的流量
def net():
    net = "cat /proc/net/xt_qtaguid/stats|grep " + uid() + "|gawk '{rx_bytes+=$6}{tx_bytes+=$8}END{print rx_bytes,tx_bytes}'"
    return net


# 获取APP的电量
def bat():
    bat = "dumpsys batterystats|grep " + pkg
    return bat


# 获取APP的FPS
def fps():
    fps = "service call SurfaceFlinger 1013"
    return fps


# 获取手机的实际物理内存总量
def total_mem():
    total_mem = utils.shell("cat /proc/meminfo|grep MemTotal").stdout.readlines()
    return total_mem

if __name__ == '__main__':
    pass
