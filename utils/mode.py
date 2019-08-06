# -*- coding:utf8 -*-

'''
    @Author: Victor Chen
    @File  :  mode.py
    @Description:
        模式的代码
'''

# 单例模式的注解
def Singleton(cls):
    """单例模式"""
    instance = {}
    def _singleton(*args, **kws):
        if cls not in instance:
            instance[cls] = cls(*args, **kws)
        return instance[cls]
    return _singleton