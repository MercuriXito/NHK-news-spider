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

# 对连接应该使用单例模式
def Singleton(cls):
    """单例模式"""
    instance = {}
    def _singleton(*args, **kws):
        if cls not in instance:
            instance[cls] = cls(*args, **kws)
        return instance[cls]
    return _singleton

@Singleton
class Connection:
    """单连接类"""
    def __init__(self):
        super().__init__()
        self.conn = None

    def getConn(self):
        if self.conn is None:
            self.conn = pymysql.connect(
                host = 'localhost', 
                user='root',
                password='taylor01', 
                db='nhknews', 
                charset='utf8'
                )
        return self.conn

    def closeConn(self):
        if self.conn is not None:
            self.conn.close()

def getConn():
    return Connection().getConn()

def closeConn():
    Connection().closeConn()