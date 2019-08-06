# -*- coding:utf8 -*-

'''
    @Author: Victor Chen
    @File  :  start.py
    @Description: start.py 现在作为爬取程序的主入口

'''

from spider import route
from dao import DaoConfig

route.scrapeMain()
DaoConfig.closeConn()
