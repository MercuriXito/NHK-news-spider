# -*- coding:utf8 -*-

'''
    @Author: Victor Chen
    @File  :  DaoDescWords.py
    @Description:
        为DescWords实体类提供的数据修改的操作类
'''

import pymysql

from dao.DaoConfig import getConn
from entity.DescWords import DescWords

conn = getConn()

def insert(descWords):

    try:
        with conn.cursor() as cursor:
            sql = "INSERT INTO `wordsdesc`(`wordsMain`,`wordsDesc`,`wordsHash`) " + \
            "VALUES('"+ descWords.wordsMain +"','"+ descWords.wordsDesc +"',MD5('"+ descWords.wordsMain +"'))"

            cursor.execute(sql)
        
        conn.commit()

    except Exception as e:
        conn.rollback()
        print(sql)
        print(descWords)
        print("Error:{}".format(e))
        

    pass


def searchByVarcharField(keyword, value):
    """allowedField: ['wordsMain','wordsHash','wordsDesc'] """

    sql = "SELECT `wordsId`, `wordsMain`, `wordsDesc` FROM wordsdesc"

    allowedField = ["wordsMain","wordsHash","wordsDesc"]
    if keyword not in allowedField:
        print("Wrong Quering Field[{}]".format(keyword))
        return []

    result = []
    try:
        with conn.cursor() as cursor:
            sql += " WHERE "+ keyword +" = '"+ value +"';"
            cursor.execute(sql)
            result = cursor.fetchall()
    except Exception as e:
        print(sql)
        print("Error:{}".format(e))
    
    return result


def searchLikeVarcharField(keyword, value):
    """allowedField: ['wordsMain','wordsDesc'] """

    sql = "SELECT `wordsId`, `wordsMain`, `wordsDesc` FROM wordsdesc"

    allowedField = ["wordsMain","wordsDesc"]
    if keyword not in allowedField:
        print("Wrong Quering Field[{}]".format(keyword))
        return []

    result = []
    try:
        with conn.cursor() as cursor:
            sql += " WHERE "+ keyword + " like '%"+ value +"%' ;"
            cursor.execute(sql)
            result = cursor.fetchall()
    except Exception as e:
        print(sql)
        print("Error:{}".format(e))
    
    return result


def insertWordsInNewsById(postsId, wordsId):

    sql = "INSERT INTO `wordsinposts`(`postsId`,`wordsId`)"
    try:
        sql += "VALUES(%d,%d);" %(postsId, wordsId)
        with conn.cursor() as cursor:
            cursor.execute(sql)
        
        conn.commit()
    except Exception as e:
        print(sql)
        conn.rollback()
        print("Error:{}".format(e))

    return True

def seachWordsInNewsById(postsId):

    sql = ""

    pass