# -*- coding:utf8 -*-

'''
    @Author: Victor Chen
    @File  :  DaoConfig.py
    @Description:
        配置数据库连接
'''

import os,sys
sys.path.append(os.path.abspath(os.curdir))

import pymysql

from config.configuration import pconfig
from utils.mode import Singleton

# 数据库的连接类，行为是单例模式
@Singleton
class Connection:
    def __init__(self):
        super().__init__()
        self.conn = None

    def getConn(self):
        if self.conn is None:
            cons = pconfig()
            dbcon = cons.get_config()["database-config"]
            self.conn = pymysql.connect(
                host = dbcon["host"],
                user= dbcon["username"],
                password= dbcon["password"], 
                db=dbcon["dbname"], 
                charset=dbcon["charset"]
                )
        return self.conn

    def closeConn(self):
        if self.conn is not None:
            self.conn.close()

def getConn():
    return Connection().getConn()

def closeConn():
    Connection().closeConn()