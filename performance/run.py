# coding=utf-8
from time import sleep
from scriptUtils import excel, utils
from getData import cpu, memory, fps, net, excutecpu, batteryTemp, cpuTemp


ex = excel.WriteDate()  # 实例化一个ex写入对象
pkg = "com.longtu.weifuhua"

# 启动采集数据线程
ecpu = excutecpu.WeiFuHua()
cpuinfo = cpu.CpuData(pkg)
meminfo = memory.MemoryData(pkg)
fpsinfo = fps.RootFpsData()
netinfo = net.NetData(pkg)
bttinfo = batteryTemp.BatteryTempData()
ctpinfo = cpuTemp.CpuTempData()

ecpu.start()

cpuinfo.start()
meminfo.start()
fpsinfo.start()
netinfo.start()
bttinfo.start()
ctpinfo.start()

utils.stop = (bool(raw_input("敲回车停止：")))

ecpu.join()
cpuinfo.join()
meminfo.join()
fpsinfo.join()
netinfo.join()
bttinfo.join()
ctpinfo.join()


# 写入数据
ex.writeData(sheet_name=u"设备信息", heads=[], data=[])

ex.writeData(sheet_name=u"CPU使用率", heads=[u"CPU(%)"], data=cpuinfo.get_cpu())

ex.writeData(sheet_name=u"内存占用率",
             heads=[u"Pss Total(KB)", u"Private Dirty", u"Private Clean", u"Swapped Dirty", u"Heap Size", u"Heap Alloc",
                    u"Heap Free"], data=meminfo.get_mem())

ex.writeData(sheet_name=u"FPS帧率", heads=[u"fps"], data=fpsinfo.get_fps())

ex.writeData(sheet_name=u"流量", heads=[u"net(KB)"], data=netinfo.get_net())

ex.writeData(sheet_name=u"电池温度", heads=[u"battery temp(℃)"], data=bttinfo.get_battery_temp())

ex.writeData(sheet_name=u"CPU温度", heads=[u"cpu temp(℃)"], data=ctpinfo.get_cpu_temp())


# 关闭excel
ex.close()
