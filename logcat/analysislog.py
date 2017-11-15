# -*- condig:utf-8 -*-
from contextlib import nested
import re


class AnalysysLogcat(object):
    """docstring for  AnalysysLogcat"""
    def __init__(self):
        self.want_get_time = None
        self.before_want_time = None

    def date_processed(self,date_str):
        self.want_get_time = "13:54:34"
        split_time_str = self.want_get_time.split(":")
        hour = int(split_time_str[0])
        minute = int(split_time_str[1])
        second = int(split_time_str[2])
        if minute < 10:
            hour = hour -1
            minute = 60 - (10 -minute)
        elif minute == 10:
            minute = str("00")
        else:
            minute = minute - 10

        self.before_want_time = ":".join((str(hour),str(minute),split_time_str[2]))
        print self.before_want_time,self.want_get_time

    def do_analysis_work(self):
        all_logcat_path = "adb_logcat.log"
        some_logcat_path = "logcat.log"
        with nested(open(some_logcat_path,"w+"),open(all_logcat_path)) as (some_log,all_log):
            if_hava = False
            for file_read_lines in all_log:
                if re.search(self.before_want_time, file_read_lines):
                    some_log.write(file_read_lines)
                    if_hava = True
                elif re.search(self.want_get_time, file_read_lines):
                    if_hava = False
                    break
                elif if_hava :
                    some_log.write(file_read_lines)


if __name__ == "__main__":
    a = AnalysysLogcat()
    a.date_processed("date_str")
    a.do_analysis_work()

