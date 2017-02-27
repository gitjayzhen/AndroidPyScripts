# -*- coding: utf-8 -*-
from matching import *

#日志解析函数
def func():
    para_value = [None]*50    #固定数组，用于存储解析出的参数名
    f = open("YKAdebug_sendCache.txt")    #打开本地log
    l =[None]*50   #固定数组，存储每一个事件的每一行数据
    #losedpara=[None]*30
    line = (f.readline()).decode('utf-8')   #按行读取
    mark = -1   #事件类型参数在数组中的索引
    n = -1   #事件名称参数在数组中的索引
    para_i = 0
    i = 0
    extend = -1
    rc = -1
    while True:
      #print line
      if len(line) == 0:    #判断日志内容是否结束
         break
      if cmp(line.strip(),'}') == 0  or cmp(line.strip(),'}, {') == 0:
         j=0
         if "A5" in l[mark]:
             identifying(l,extend,rc,n)    #如果是A5事件，进行参数匹配
         i = 0
         para_i = i
      line = (f.readline()).decode('utf-8')
      l[para_i] = line
      if cmp(line.strip(),'}') != 0 and cmp(line.strip(),'}, {') != 0 and len(line) != 0 and cmp(line.strip(),'{') != 0:
         npos = line.index(':')
         s1 = line[1:npos]   #按照“：”对字符串进行截取
         s2 = line[npos+1:len(line)]

         if cmp(s1.strip(),'"t1"') == 0:
            mark=i
         if cmp(s1.strip(),'"e"') == 0:
             extend=i
         if cmp(s1.strip(),'"rc1"') == 0:
             rc=i
      if "n3" in line:
        n = i
        #print n
      i = i+1
      para_i = i
    f.close()



if __name__=='__main__':
    func()
