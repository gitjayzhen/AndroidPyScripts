# coding=utf-8
from time import sleep
from scriptUtils import utils
import threading


class NetData(threading.Thread):
    def __init__(self, pkg):
        super(NetData, self).__init__()
        self.ls = []
        self.pkg = pkg

    def run(self):
        """
        基于UID获取App的网络流量的方法
        从/proc/net/xt_qtaguid/stats获取网络流量统计，进行判断
        """
        while True:
            if utils.stop!=True:
                break
            sleep(1)
            totalNet = []
            flag_net = utils.shell("cat /proc/net/xt_qtaguid/stats").stdout.readline()
            if "No such file or directory" not in flag_net:
                list_rx = []  # 接收网络数据流量列表
                list_tx = []  # 发送网络数据流量列表

                str_uid_net_stats = utils.shell(
                    "cat /proc/net/xt_qtaguid/stats|findstr %s" % utils.get_app_uid(
                        self.pkg)).stdout.readlines()
                try:
                    for item in str_uid_net_stats:
                        rx_bytes = item.split()[5]  # 接收网络数据流量
                        tx_bytes = item.split()[7]  # 发送网络数据流量
                        list_rx.append(int(rx_bytes))
                        list_tx.append(int(tx_bytes))
                    tm = utils.timestamp()
                    floatTotalNetTraffic = (sum(list_rx) + sum(list_tx)) / 1024.0 / 1024.0
                    floatTotalNetTraffic = round(floatTotalNetTraffic, 2)
                    # print "接受：", list_rx
                    # print "发送：", list_tx
                    # print "总消耗：%sKB" % floatTotalNetTraffic
                    totalNet.append(floatTotalNetTraffic)
                    totalNet.insert(0, tm)
                    self.ls.append(totalNet)
                except:
                    print "[ERROR]: cannot get the /proc/net/xt_qtaguid/stats"
                    return 0.0
            else:
                strTotalTxBytes = utils.shell(
                    "cat proc/uid_stat/%s/tcp_snd" % utils.get_app_uid(self.pkg)).stdout.readline()
                strTotalRxBytes = utils.shell(
                    "cat proc/uid_stat/%s/tcp_rcv" % utils.get_app_uid(self.pkg)).stdout.readline()
                try:
                    tm = utils.timestamp()
                    floatTotalTraffic = (int(strTotalTxBytes) + int(strTotalRxBytes)) / 1024.0 / 1024.0
                    floatTotalTraffic = round(floatTotalTraffic, 2)
                    # print "总消耗：%sKB" % floatTotalTraffic
                    totalNet.append(floatTotalTraffic)
                    totalNet.insert(0, tm)
                    self.ls.append(totalNet)
                except:
                    return 0.0

    def get_net(self):
        return self.ls
