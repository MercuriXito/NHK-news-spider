# -*- coding:utf8 -*-

'''
    @Author: Victor Chen
    @File  :  EasyNewsStoreService1.py
    @Description:

'''
from dao.DaoTable import *
from entity.DangoMean import DangoMean
from entity.EasyNewsT import EasyNews

import hashlib
from datetime import datetime
from datetime import date

def store_one_news(news, dangomeans):

    # 查询news的id
    epostQuery = query_by_condition_func("EasyPosts")
    eid = epostQuery(["postNewsId"],[1],[news.news_id])

    # 不重复再插入
    if len(eid) == 0:
        # 插入news
        epostInsert = insert_func("EasyPosts")
        epostInsert(
            ["postNewsId","postTitle","postPublishTime","postContent","postType","hasImg","hasAudio","imgName","audioName"],
            [
                news.news_id,
                news.title,
                news.publish_time,
                news.content,
                news.type,
                news.has_img,
                news.has_audio,
                news.img_name,
                news.audio_name
            ]
        )
        eid = epostQuery(["postNewsId"],[1],[news.news_id])

    eid = eid[0][0]


    # 初始化函数
    dangoInsert = insert_func("DangoMeans")
    dangoQuery = query_by_condition_func("DangoMeans")

    dids = []
    for dangomean in dangomeans:
        did = dangoQuery(["totalHash"],[1],[dangomean.hash])
        if len(did) == 0:
            dangoInsert(
                ["dango","mean","totalHash"],
                [
                    dangomean.dango,
                    dangomean.mean,
                    dangomean.hash
                ]
            )
            did = dangoQuery(["totalHash"],[1],[dangomean.hash])
        
        did = did[0][0]
        dids.append(did)

    # 关联插入
    dinpostInsert = insert_func("DangoInPosts")
    dinpostQuery = query_by_condition_func("DangoInPosts")
    for did in dids:
        res = dinpostQuery(["postId","dangoId"],[1,1],[eid, did])
        if len(res) == 0:
            dinpostInsert(["postId","dangoId"],[eid, did])

    pass