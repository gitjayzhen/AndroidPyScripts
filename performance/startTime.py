# -*- coding: utf-8 -*-
from time import sleep
from scriptUtils import utils


app_time = []
system_time = []
app_start_time = utils.shell("am start -W -n com.longtu.weifuhua/com.longtu.weifuhua.ui.homepage.activity.ServiceActivity").stdout.readlines()[4:6]

result = []
for i in app_start_time:
    result.append(i.split()[1])

app_time.append(result[0])
system_time.append(result[1])

print "APP自身启动耗时：", app_time
print "系统启动APP耗时：", system_time

utils.kill_application("com.longtu.weifuhua")
