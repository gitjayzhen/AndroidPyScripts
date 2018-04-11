# coding=utf-8
from time import sleep
from scriptUtils import utils


class FpsResult:
    def __init__(self):
        pass

    def gfxinfo(self):
        # 获取绘制帧的时间数组
        times = utils.shell(
            "dumpsys gfxinfo com.longtu.weifuhua|gawk '/Execute/,/View hierarchy/'|gawk NF'{print $1,$2,$3,$4}'|grep -v '^Draw'|grep -v '^View hierarchy'").stdout.readlines()

        # 计算帧数量
        frame_count = len(times)

        # 计算绘制每一帧的总时间，单位:ms
        count_time = []
        for gfx in times:
            time = gfx.split()
            sum_time = float(time[0]) + float(time[1]) + float(time[2]) + float(time[3])
            count_time.append(sum_time)

        return frame_count, count_time

    def result(self):
        gfxinfo_tuple = self.gfxinfo()
        frames = gfxinfo_tuple[0]
        seconds = gfxinfo_tuple[1]
        # print "原始数据：", gfxinfo_tuple
        print "绘制 %s 帧" % frames
        # print "时间数组：", seconds
        second = 0.0
        for t in seconds:
            second += t
        print "耗时：%sms" % second
        if second == 0.0:
            print "0 FPS"
        else:
            f = int(1000 / second)

            print "%s FPS\n" % f


if __name__ == '__main__':
    fps = FpsResult()
    for i in range(10):
        sleep(1)
        fps.result()
