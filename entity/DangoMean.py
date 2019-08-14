# -*- coding:utf8 -*-

'''
    @Author: Victor Chen
    @File  :  DangoMeaning.py
    @Description:
        单个单词释义词条的实体类
'''

"""
DangoMean 实体类应该具有的属性：
    id, dango, mean,
    hash ( mean字段的HASH值，用于索引? )    
"""

import hashlib

class DangoMean:
    def __init__(self):
        self.id = 0
        self.dango = ""
        self.mean = ""
        self.generate_hash()
    
    # DangoMean dango 和 mean 被修改之后一定要重新生成hash
    def generate_hash(self, encoding="utf-8"):
        vars = self.dango + self.mean
        vars = vars.encode(encoding)
        res = hashlib.md5(vars)
        self.hash = res.hexdigest()

    