# -*- coding: utf-8 -*-
import xdrlib
import xlrd
import xlwt
import sys
def identifying(array,ext_index,rc_index,n):
    data = xlrd.open_workbook('testdata.xlsx')
    pos = array[rc_index].index(':')    #
    rc1_value = array[rc_index][pos+1:len(array[rc_index])]
    pos = array[ext_index].index(':')
   # print array[ext_index]
    ext_value = array[ext_index][pos+1:len(array[ext_index])]
    #print ext_value
    pos = array[n].index(':')
    nam = array[n][pos+2:len(array[n])-2].strip()
    i = 0
    flag = 0
    a = [0]*15
    num = 0
    table = data.sheets()[i]
    nrows = table.nrows
    ncols = table.ncols
    for j in range (1,nrows):    #the first row is used
        name = table.cell(j,2).value
        value_para = table.cell(j,8).value.split('\n')
        excel_rc1 = table.cell(j,3).value.strip()
        if excel_rc1 != '' and excel_rc1 in rc1_value:
            if ext_value.strip() == '':
                print name+':Null\n'
            else:
                ext_value = ext_value[2:len(ext_value)-3]
                ext_value = ext_value.split('&')
                num=0
                for value in value_para:
                    splitvalue = value.strip().split('=')
                    for ext in ext_value:
                        splitext = ext.split('=')
                        #print splitext[0]
                        #print "%s and %s\n"%(splitext[0],splitvalue[0].strip())
                        if cmp(splitvalue[0].strip(),splitext[0]) == 0:
                            flag = 1
                            a[num] = 1
                            num = num+1
                            print "%s"%ext
                            break
                        else:
                            flag = 0
                    if flag == 0:
                        print "%s:Wrong!Find a missing parameter\n"%nam
                        break
                if flag == 1:
                        print "%s:Right!\n"%nam
                break

