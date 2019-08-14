# -*- coding:utf8 -*-

'''
    @Author: Victor Chen
    @File  :  DaoEasyNews.py
    @Description:
        为EasyNews实体类提供的数据修改的操作类
'''

import pymysql

from datetime import datetime
import time

from utils.annotations import threadLock
from dao.DaoConfig import getConn
from entity.EasyNews import EasyNews

conn = getConn()

@threadLock
def insert(easyNews):

    try:
        with conn.cursor() as cursor:
            sql = "INSERT INTO `posts`(`postsNewsId`,`postsType`,`postsTitle`,`postsPublishTime`,`postsMain`) " \
                + "VALUES('"+ easyNews.newsId +"',1,'"+ easyNews.title +"','"+ easyNews.publishTime +"','"+ easyNews.content +"')"
            cursor.execute(sql)
        
        # commit 
        conn.commit()

    except Exception as e:
        conn.rollback()
        print(sql)
        print(easyNews)
        raise e

    pass


def search(easyNews, keywords):

    sql = "Select postsNewsId,postsType,postsTitle,postsPublishTime,postsMain from posts"

    with conn.cursor() as cursor:
        cursor.execute(sql)
        result = cursor.fetchall()
        print(result)

    pass


def searchByIntField(keyword, value):
    """ 精确查询 id, type 字段"""
    sql = "Select postsId,postsNewsId,postsType,postsTitle,postsPublishTime,postsMain from posts"

    allowedField = ["postsId","postsType"]
    if keyword not in allowedField:
        print("Wrong Quering Field[{}]".format(keyword))
        return []

    result = []
    try:
        with conn.cursor() as cursor:

            sql += " WHERE " + keyword + " = " + value + ";"
            cursor.execute(sql)
            result = cursor.fetchall()
    
    except Exception as e:
        print(sql)
        print("Error:{}".format(e))

    return result


def searchByVarcharField(keyword, value):
    """ 精确查询 postsNewsId 字段"""
    sql = "Select postsId,postsNewsId,postsType,postsTitle,postsPublishTime,postsMain from posts"

    allowedField = ["postsNewsId"]
    if keyword not in allowedField:
        print("Wrong Quering Field[{}]".format(keyword))
        return []
    
    result = []
    try:
        with conn.cursor() as cursor:

            sql += " WHERE " + keyword + " = '" + value + "';"
            cursor.execute(sql)
            result = cursor.fetchall()
    
    except Exception as e:
        print(sql)
        print("Error:{}".format(e))

    return result


def searchLikeVarcharField(keyword, value):
    """ 模糊查询 postsNewsId, postsTitle, postsMain 字段"""
    sql = "Select postsId,postsNewsId,postsType,postsTitle,postsPublishTime,postsMain from posts"

    allowedField = ["postsNewsId","postsTitle","postsMain"]
    if keyword not in allowedField:
        print("Wrong Quering Field[{}]".format(keyword))
        return []
    
    result = []
    try:
        with conn.cursor() as cursor:

            sql += " WHERE " + keyword + " like '%" + value + "%';"
            cursor.execute(sql)
            result = cursor.fetchall()
    
    except Exception as e:
        print(sql)
        print("Error:{}".format(e))

    return result


def searchByTime(date):
    """按日期查询，必须传入一个datetime类型的日期"""

    format = "%Y-%m-%d"
    datestr = date.strftime(format)

    sql = "Select postsId,postsNewsId,postsType,postsTitle,postsPublishTime,postsMain from posts"

    result = []
    try:
        with conn.cursor() as cursor:

            sql += "where DATEDIFF(postsPublishTime," + datestr + ") = 0;"
            cursor.execute(sql)
            result = cursor.fetchall()
    
    except Exception as e:
        print(sql)
        print("Error:{}".format(e))
    
    return result


def searchBetweenTime(beginDate = None, endDate = None):
    """查询时间范围"""

    format = "%Y-%m-%d"
    sql = "Select postsId,postsNewsId,postsType,postsTitle,postsPublishTime,postsMain from posts"
 
    result = []
    try:
        with conn.cursor() as cursor:

            sql += " WHERE 1=1 "
            if beginDate is not None:
                sql += "and postsPublishTime > '"+ beginDate.strftime(format) +"'"
            if endDate is not None:
                sql += "and postsPublishTime < '"+ endDate.strftime(format) +"'"
            sql += ";"

            cursor.execute(sql)
            result = cursor.fetchall()
    
    except Exception as e:
        print(sql)
        print("Error:{}".format(e))

    return result