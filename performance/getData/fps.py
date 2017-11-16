# -*- coding: utf-8 -*-
import time
import datetime
import xlsxwriter
import threading
from scriptUtils import utils
from scriptUtils.pylib import android_commands
from scriptUtils.pylib.perf import surface_stats_collector


class RootFpsData(threading.Thread):
    def __init__(self):
        super(RootFpsData, self).__init__()
        self.time_before = None
        self.time_after = None
        self.surface_before = None
        self.surface_after = None
        self.ls = []

    def get_frame_data(self):
        """
        获取帧数据及时间戳
        :return:字典
        """
        result = utils.shell("su -c 'service call SurfaceFlinger 1013'").stdout.readline()
        cur_surface = int(result.split("(")[1].split()[0], 16)
        return {"surface": cur_surface, "timestamp": time.time()}

    def run(self):
        user = utils.shell("su -c 'ls'").stdout.readline()  # 检查手机是否可以ROOT用户执行命令

        if "not found" in user:  # 非ROOT手机执行该方式
            serial_number = utils.get_serialno()
            command = android_commands.AndroidCommands(serial_number)
            collector = surface_stats_collector.SurfaceStatsCollector(command)
            collector.DisableWarningAboutEmptyData()
            collector.Start()
            while True:
                if utils.stop != True:
                    break
                tm = utils.timestamp()
                results = collector.SampleResults()
                fpsdata = []
                if not results:
                    pass
                else:
                    for i in results:

                        if i.name == "avg_surface_fps":
                            if i.value == None:
                                fpsdata.insert(0, tm)
                                fpsdata.append(0)

                            else:
                                fpsdata.insert(0, tm)
                                fpsdata.append(i.value)
                self.ls.append(fpsdata)
            collector.Stop()

        else:  # ROOT手机执行该方式
            value1 = self.get_frame_data()
            self.time_before = value1["timestamp"]
            self.surface_before = value1["surface"]
            while True:
                if utils.stop != True:
                    break
                y = []
                time.sleep(1)
                value2 = self.get_frame_data()
                self.time_after = value2["timestamp"]
                self.surface_after = value2["surface"]
                time_difference = int(round((self.time_after - self.time_before), 2))
                frame_count = (self.surface_after - self.surface_before)
                tm = utils.timestamp()
                fps = int(frame_count / time_difference)
                y.append(fps)
                self.time_before = self.time_after
                self.surface_before = self.surface_after
                y.insert(0, tm)
                self.ls.append(y)
                # print "refresh:%ss  " % time_difference, "FPS:%s" % fps

    def get_fps(self):
        return self.ls


if __name__ == '__main__':
    fps = RootFpsData(10)
    fps.run()
