# coding=utf-8
import unittest
from scriptUtils.MeThod import MeThod
from time import sleep
import threading
from scriptUtils import utils


class WeiFuHua(threading.Thread):
    def __init__(self):
        super(WeiFuHua, self).__init__()
        self.driver = MeThod()
        self.driver.api.implicitly_wait(60)  # 查找元素超时，秒

    def tearDown(self):
        self.driver.api.quit()

    def swipeToDown(self):
        width = self.driver.api.get_window_size()["width"]  # 屏幕宽度
        height = self.driver.api.get_window_size()["height"]  # 屏幕高度
        self.driver.api.swipe(width / 2, float(height / 1.02), width / 2, height / 8, 2000)  # 滑动轨迹

    def run(self):
        self.driver.findElement("xpath", "7").click()  # 点击资讯按钮
        i = 0
        while True:
            if utils.stop != True:
                break
            i += 1
            print "执行第：%d 次" % i
            self.driver.findElement("xpath", "8").click()  # 进入资讯详情
            sleep(1)
            for n in range(2):  # 滑动资讯详情页面到底部
                self.swipeToDown()
            self.driver.api.keyevent(4)  # 点击返回按钮

        self.tearDown()


if __name__ == '__main__':
    wfh = WeiFuHua()
    wfh.start()
    wfh.join()
