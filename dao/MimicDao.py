# -*- coding:utf8 -*-

'''
    @Author: Victor Chen
    @File  :  MimicDao.py
    @Description:

        写的辣鸡框架

'''

from entity.EasyNewsT import EasyNews
from dao.DaoConfig import getConn
from utils.annotations import *

import time
from datetime import datetime


"""

    requests_dict 的格式:
    request_dict = {
        "ref": ,
        "type": ,
        "fields": [],
        "values": [],
        "operate": [],
    }

    parameters 说明:
        + ref: 对应table的继承Ref类的对象，它将是参考
        + type: request_dict 指定的sql类型，合法值为[0 - 3] 分别表示为
            0 : query,
            1 : insert,
            2 : update,
            3 : delete
        
        + fields: sql中需要指明的目标字段
        + values: sql中可能用到的fields的值，如果没有使用""占位
        + operate: 对应 field 可能的操作，四种sql对应的操作如下：
            query: (1) "display" : 选择 select的可能字段 [不需要value]
                   (2) WHERE 条件： [ 需要value ]
                        "c1" : 精确查找  
                        "c2" : 模糊查找
            insert: (1) "insert" : 选择需要插入的字段的值 [需要value]
            delete: (1) 同query的WHERE条件
            update: (1) "update" : 选择需要修改的字段的值 [需要value]
                    (2) 同query的WHERE条件
                        

"""

# Ref类提供对所有给定的fields生成指定的dict的封装函数，它根据
# dbname, fields, fields_type 三个参数生成，使用时自定义的ref要继承Ref类

class Ref:
    """ 基础数据表ref类 """
    def __init__(self):
        self.dbname = ""
        self.fields = []
        self.fields_type = []

    def index_str2int(self, str_indices = None):
        """ 将字符的field转化为request_ref中int类型的下标定位 """

        if str_indices is None:
            return list(range(len(self.fields)))

        int_indices = []
        for index in str_indices:
            try:
                ind = self.fields.index(index)
                int_indices.append(ind)
            except ValueError:
                print("Invalid index:{}".format(index))
                continue

        return int_indices
    
    def sqlfy_field_value(self, field_selector, value):
        """ 对照field的type属性格式化value的字符串 """
        if self.fields_type[field_selector] == 1:
            return "`" + value + "`"
        else:
            return str(value)


    def fill_len_val(self, flist, val=""):
        """生成和flist长度相同的值全部为val的列表,val的值默认为""
        """
        return [val for i in range(len(flist))]


    @DeprecationWarning
    def select_fileds_operate(self, field_selector = None, operate = None):
        """ 由field_selector选择ref中指定的field，并返回由这些field组成的列表

            参数：
                field_selector: 如果为None选择所有列，field_selector可以是由0,1字符组成的字符串，
                表示是否选择对应顺序的field，或者是一个值，其二进制表示是否选择对应顺序的field
                operate: 现在仅仅是个字符串而已，如果为None，则不返回由operate字符组成的列表
        """

        if field_selector is None:
            fs = self.fields
        else:
            fs = self._select_field(field_selector)

        rs = [list(range(len(fs)))]
        if operate is not None:
            ops = []
            for i in range(len(fs)):
                ops.append(operate)
            rs.append(ops)

        return rs  

        
    def _select_field(self, field_selector):

        fs = []
        if isinstance(field_selector, str):
            for i,flag in enumerate(str):
                if int(flag):
                    fs.append(self.fields[i])
            return fs

        elif isinstance(field_selector, int):

            for i,flag in enumerate(bin(field_selector)[2:]):
                if int(flag):
                    fs.append(self.fields[i])
            return fs
        else:
            raise(Exception("Unspported selector:{}".format(field_selector)))


"""
    执行基本过程
"""
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
    requset_dict解析和sql拼接
"""
def dispatcher(requests_dict):

    # dispatcher 先做参数检查
    rtype = requests_dict["type"]
    if rtype not in list(range(len(_dispatcher_func))):
        raise(Exception("Illegal type of requests_dict"))

    ref = requests_dict["ref"]
    if not isinstance(ref, Ref):
        raise(Exception("Illegal parameter of ref: ref should be the subclass of `Ref`."))
        
    
    return _dispatcher_func[rtype](requests_dict)


def _insert_sql(requests_dict):
    
    ref = requests_dict["ref"]
    basic_sql = "INSERT INTO `" + ref.dbname + "` "
    
    field_strs = []
    values_strs = []

    # 根据dict检查拼接insert的sql
    for field, value, op in zip(requests_dict["fields"], requests_dict["values"],requests_dict["operate"]):
        
        if field not in list(range(len(ref.fields))):
            print("Invalid field:{}".format(field))
            continue
        
        if op == "insert":
            tstr = "`"+ ref.fields[field] + "`"
            field_strs.append(tstr)
            
            vstr = _get_ref_field_value_str(ref, field, value)
            values_strs.append(vstr)

    if len(field_strs) == 0 or len(values_strs) == 0:
        return ""

    sql = basic_sql + "(" + ",".join(field_strs) + ")"
    sql += " VALUES" + "( " + ",".join(values_strs) + " )"

    return sql 


def _update_sql(requests_dict):

    ref = requests_dict["ref"]

    update_strs = []
    condition_strs = []

    # 检查dict的operate
    for field, value, op in zip(requests_dict["fields"], requests_dict["values"],requests_dict["operate"]):

        if field not in list(range(len(ref.fields))):
            print("Invalid field:{}".format(field))
            continue

        if op == "update":
            ustr = "`" + ref.fields[field] + "`"
            ustr += "="
            ustr += _get_ref_field_value_str(ref, field, value)
            update_strs.append(ustr)
        
        # c1 是精确查询
        if op == "c1":
            cstr = "`" + ref.fields[field] + "`"
            cstr += "="
            cstr += _get_ref_field_value_str(ref, field, value)
            condition_strs.append(cstr)
        
        # c2 是模糊查询
        elif op == "c2":
            cstr = "`" + ref.fields[field] + "`"
            cstr += " LIKE "
            cstr += " '" + value + "' "
            condition_strs.append(cstr)

        sql = "UPDATE " + "`" + ref.dbname + "`"
        sql += " SET "
        sql += " " + ",".join(update_strs) + " "
        sql += " WHERE 1=1 "

        if len(update_strs) == 0:
            return ""
        if len(condition_strs) == 0:
            return sql
        
        sql += " AND " + " AND ".join(condition_strs)
    
    return sql


def _query_sql(requests_dict):

    ref = requests_dict["ref"]

    target_strs = []
    condition_strs = []

    # 检查dict的operate
    for field, value, op in zip(requests_dict["fields"], requests_dict["values"],requests_dict["operate"]):

        if field not in list(range(len(ref.fields))):
            print("Invalid field:{}".format(field))
            continue

        if op == "display":
            tstr = "`" + ref.fields[field] + "`"
            target_strs.append(tstr)
            continue
        
        # c1 是精确查询
        if op == "c1":
            cstr = "`" + ref.fields[field] + "`"
            cstr += "="
            cstr += _get_ref_field_value_str(ref, field, value)
            condition_strs.append(cstr)
        
        # c2 是模糊查询
        elif op == "c2":
            cstr = "`" + ref.fields[field] + "`"
            cstr += " LIKE "
            cstr += " '" + value + "' "
            condition_strs.append(cstr)

    sql = "SELECT"
    sql += " " + ",".join(target_strs) + " "
    sql += "FROM `" + ref.dbname + "` WHERE 1=1 "

    if len(target_strs) == 0:
        return ""
    if len(condition_strs) == 0:
        return sql

    # 这里的条件没有抓好
    sql += " AND " + " AND ".join(condition_strs)

    return sql


def _delete_sql(requests_dict):

    ref = requests_dict["ref"]
    del_cond_strs = []

    # 检查dict的operate
    for field, value, op in zip(requests_dict["fields"], requests_dict["values"],requests_dict["operate"]):

        if field not in list(range(len(ref.fields))):
            print("Invalid field:{}".format(field))
            continue
        
        # c1 是精确查询
        if op == "c1":
            cstr = "`" + ref.fields[field] + "`"
            cstr += "="
            cstr += _get_ref_field_value_str(ref, field, value)
            del_cond_strs.append(cstr)
        
        # c2 是模糊查询
        elif op == "c2":
            cstr = "`" + ref.fields[field] + "`"
            cstr += " LIKE "
            cstr += " '" + value + "' "
            del_cond_strs.append(cstr)

    sql = "DELETE FROM " + "`" + ref.dbname + "` WHERE 1 = 1"

    if len(del_cond_strs) == 0:
        return sql

    # 这里的条件没有抓好
    sql += " AND " + " AND ".join(del_cond_strs)

    return sql


# 全局的执行函数
def execute(requests_dict):

    rtype = requests_dict["type"]
    sql = dispatcher(requests_dict)

    if sql == "":
        raise(Exception("SQL not executed for incorrect request dict:{}".format(requests_dict)))


    print("\n{}\n".format(sql))

    if rtype == 0:
        return _basic_query(sql)

    elif rtype in list(range(1,4)):
        return _basic_execute(sql)

"""
    辅助函数和变量:

"""

# 检查ref中的固定的字段的格式化属性，返回对应值的格式化字符串
def _get_ref_field_value_str(ref, field, value):
    if ref.fields_type[field] == 1:
        return "`" + value + "`"
    else:
        return str(value)


_dispatcher_func = {
    0 : _query_sql,
    1 : _insert_sql,
    2 : _update_sql,
    3 : _delete_sql,
}
