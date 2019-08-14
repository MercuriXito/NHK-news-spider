# -*- coding:utf8 -*-

'''
    @Author: Victor Chen
    @File  :  start.py
    @Description: start.py 现在作为爬取程序的主入口

'''

from spider import route2
from dao import DaoConfig

try:
    route2.scrapeMain()
except Exception as ex:
    raise(ex)
finally:
    DaoConfig.closeConn()
