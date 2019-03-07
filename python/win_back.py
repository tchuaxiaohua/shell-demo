#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019/3/6 14:18
# @Author  : tchua
# @Email   : tchuaxiaohua@163.com
# @File    : win_back.py
# @Software: PyCharm
import os,time
import zipfile

DATE = time.strftime("%Y-%m-%d")
BACK_UP = "E:/Pycharm/test/"
SOURCE_FILE = "E:/Pycharm/shell"
ZIPNAME = BACK_UP + DATE + '_oa.zip'
print(ZIPNAME)
if  not os.path.exists(BACK_UP):
    os.makedirs(BACK_UP)

def addzip(zipfilename):
    f = zipfile.ZipFile(zipfilename,'w')
    for dirpath,dirnames,filenames in os.walk(SOURCE_FILE):
        for filename in filenames:
            f.write(os.path.join(dirpath,filename))
    f.close()
addzip(ZIPNAME)
