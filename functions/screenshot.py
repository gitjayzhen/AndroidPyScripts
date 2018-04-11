#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

from utils import androiddebug

# 截取当前屏幕，截屏文件保存至当前目录下的screen文件夹中

PATH = lambda p: os.path.abspath(p)


def screenshot():
    path = PATH("%s/screenshot" % os.getcwd())
    androiddebug.shell("screencap -p /data/local/tmp/tmp.png").wait()
    if not os.path.isdir(path):
        os.makedirs(path)

    androiddebug.adb("pull /data/local/tmp/tmp.png %s" % PATH("%s/%s.png" % (path, androiddebug.timestamp()))).wait()
    androiddebug.shell("rm /data/local/tmp/tmp.png")

if __name__ == "__main__":
    screenshot()
    print "success"
