# -*- coding:utf8 -*-

'''
    @Author: Victor Chen
    @File  :  DaoTable.py
    @Description:
        EasyNews 实体类的dao层

        dao层实现单个表的结构的操作，
        不和table的结构耦合，实现复用
'''

from dao.DaoConfig import getConn

def _basic_query(sql):
    """ 执行查询的sql的基本过程 """
    con = getConn()
    try:
        with con.cursor() as cursor:
            cursor.execute(sql)
            result = cursor.fetchall()
    except Exception as ex:
        print(sql)
        print("Error:{}".format(ex))
        return []

    return result


def _basic_execute(sql):
    """ 执行非查询sql的基本过程 """
    con = getConn()
    try:
        with con.cursor() as cursor:
            cursor.execute(sql)

        con.commit()

    except Exception as ex:
        con.rollback()
        print(sql)
        print("Error:{}".format(ex))
        return False

    return True

"""
    简单点好吧
"""
# 查询所有, 等于query_by_condition()
def query_all_func(tbname):
    def _query_all():
        sql = "SELECT * FROM `" + tbname + "`"
        return _basic_query(sql)
    return _query_all

# 组成查询条件的sql
def form_cond_str(fields, cond_types, vals):
    cond_sql = " WHERE 1=1"

    condstrs = []
    for field, cond_type, val in zip(fields, cond_types, vals):
        condstr = "`" + field + "`"
        
        if cond_type == 1:
            condstr += "="
        elif cond_type == 2:
            condstr += " < "
        elif cond_type == 3:
            condstr += " > "
        else:
            condstr += " LIKE "

        if isinstance(val, int):
            condstr += str(val)
        elif isinstance(val, str):
            condstr += "'" + val + "'"
        
        condstrs.append(condstr)

    if len(condstrs) > 0 :
        cond_sql += " AND " + " AND ".join(condstrs)

    return cond_sql


# 多条件查询
def query_by_condition_func(tbname):
    def _query_by_condition(query_fields = [], cond_types = [], vals = []):
        """
        cond_types 为 1 代表精确查询，为0代表模糊查询, 2代表小于号, 3代表大于号
        """
        sql = "SELECT * FROM  `" + tbname + "`"
        return _basic_query(sql + form_cond_str(query_fields, cond_types, vals))

    return _query_by_condition

# 插入
def insert_func(tbname):
    def _insert(fields, vals):

        sql = "INSERT INTO `" + tbname + "`"

        fstrs = []
        for field in fields:
            fstrs.append("`" + field + "`")

        vstrs = []
        for val in vals:
            if isinstance(val, int):
                vstrs.append(str(val))
            elif isinstance(val, str):
                vstrs.append("'" + val + "'")

        sql += " (" + ",".join(fstrs) + ") "
        sql += "VALUES(" + ",".join(vstrs) + ")"

        return _basic_execute(sql)

    return _insert

# 删除
def delete_func(tbname):
    def _delete(fields = [], cond_types = [], vals = []):
        sql = "DELETE FROM `" + tbname + "`"
        return _basic_query(sql + form_cond_str(fields, cond_types, vals))

    return _delete