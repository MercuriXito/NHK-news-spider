# -*- coding:utf8 -*-

'''
    @Author: Victor Chen
    @File  :  annotations.py
    @Description:
        实用的注解

'''

import threading

# 互斥锁
def threadLock(func):
    """互斥锁，保证函数一次只有一个线程执行函数"""
    lock = threading.Lock()
    def _locked_func(*args, **kws):
        lock.acquire()
        val = func(*args, **kws)
        lock.release()
        return val

    return _locked_func


# 信号量锁，当val=1时就是互斥锁
def threadSemaphoreLock(val):
    """信号量锁，保证最多val个线程执行函数"""
    def decorate(func):
        lock = threading.Semaphore(val)
        
        def _locked_func(*args, **kws):
            lock.acquire()
            val = func(*args, **kws)
            lock.release()
            return val
        
        return _locked_func

    return decorate


# 单例模式的注解
def Singleton(cls):
    """单例模式"""
    instance = {}
    def _singleton(*args, **kws):
        if cls not in instance:
            instance[cls] = cls(*args, **kws)
        return instance[cls]
    return _singleton

