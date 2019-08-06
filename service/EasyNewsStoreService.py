# -*- coding:utf8 -*-

'''
    @Author: Victor Chen
    @File  :  EasyNewsService.py
    @Description:
        用于存储easynews的service层
'''

from dao import DaoEasyNews as endao
from dao import DaoDescWords as dworddao

from entity.EasyNews import EasyNews
from entity.DescWords import DescWords

import hashlib
from datetime import datetime
from datetime import date

def AddNews(newslist):
    """插入一系列的新闻"""
    for news in newslist:
        endao.insert(news)


def AddWords(wordslist):
    """插入wordlist，如果重复不插入"""

    for words in wordslist:
        hash = hashlib.md5(words.wordsMain)
        result = dworddao.searchByVarcharField(
            "wordsHash", hash.hexdigest())
        
        if len(result) > 0:
            continue
        
        dworddao.insert(words)

def AddNewsAndWords(news, wordslist):
    """插入一条news和它对应的wordslist"""

    # 查询news是否已经存在
    result = endao.searchByVarcharField("postsNewsId", news.newsId)
    
    if len(result) > 0:
        print("news[{}] already exists".format(news.title))
        return 
    
    endao.insert(news)
    result = endao.searchByVarcharField("postsNewsId", news.newsId)
    postsId = result[0][0]

    # 获取到news的id后插入该news中的wordlist
    for words in wordslist:
        # 先查询有没有再添加
        hash = hashlib.md5(words.wordsMain.encode("utf-8"))
        result = dworddao.searchByVarcharField(
            "wordsHash", hash.hexdigest())

        if len(result) > 0:
            wordsId = result[0][0]

        else:
            dworddao.insert(words)
            wordsId = dworddao.searchByVarcharField(
            "wordsHash", hash.hexdigest())[0][0]

        # 链接
        dworddao.insertWordsInNewsById(postsId, wordsId)

    return True
        

def getNewsAndWords(date=datetime.today()):
    """获取每一天的新闻了"""

    records = endao.searchByTime(date)

    # postsId,postsNewsId,postsType,postsTitle,postsPublishTime,postsMain
    for record in records:
        news = EasyNews()

    pass