# -*- coding:utf8 -*-

'''
    @Author: Victor Chen
    @File  :  EasyNewsRenderService.py
    @Description:
        响应前端对EasyNews数据
'''

import time
from datetime import datetime
from datetime import timedelta

from entity.EasyNewsT import EasyNews
from entity.DangoMean import DangoMean

from dao.DaoTable import *

# index页面的json
def render_index_json():

    # 获取主页的信息咯
    epquery = query_all_func("EasyPosts")
    rslist = epquery()

    message_dict = []
    
    for rs in rslist:
        news_id = rs[1]
        news_title = rs[2]
        news_date = rs[3]
        news_has_img = rs[6]
        news_img_name = rs[8]

        if not news_has_img:
            news_img_name = "logo.png"
        
        date_format = "%Y-%m-%d"

        message_dict.append({
            "news_id" : news_id,
            "detailed_url" : news_id,
            "publish_date": time.strftime(date_format, news_date.timetuple()),
            "news_title": news_title,
            "news_img_name": news_img_name,
        })

    # 最后给message_dict排序，日期后的在前面
    def choose_date(news_dict):
        return news_dict["publish_date"]

    message_dict.sort(key = choose_date, reverse = True)

    return message_dict


# 详情页的信息
def render_detailed_content(news_id):

    epQuery = query_by_condition_func("EasyPosts")
    rlist = epQuery(["postNewsId"],[1],[news_id])

    mess = {}
    if len(rlist) != 0:
        news = rlist[0]
        id = news[0]
        news_id = news[1]
        news_title = news[2]
        news_date = news[3]
        news_content = news[4]
        news_has_img = news[6]
        news_img_name = news[8]

        if not news_has_img:
            news_img_name = "logo.png"
        
        date_format = "%Y-%m-%d"

        mess = {
            "news_id" : news_id,
            "detailed_url" : news_id,
            "publish_date": time.strftime(date_format, news_date.timetuple()),
            "news_title": news_title,
            "news_content": news_content,
            "news_img_name": news_img_name,
        }

        mess["news_link_dangos"] = []

        # 查询有关的单词
        dinpostsQuery = query_by_condition_func("DangoInPosts")
        linked_dango_list = dinpostsQuery(["postId"],[1],[id])
        
        dangoQuery = query_by_condition_func("DangoMeans")
        for _,_,dango_id in linked_dango_list:
            dango = dangoQuery(["dangoId"],[1],[dango_id])[0]
            dango_dict = {
                "dango": dango[2],
                "dango_mean": dango[3]
            }

            mess["news_link_dangos"].append(dango_dict)

    return mess

def render_index_time_range_json(time_range):

    # 获取主页的信息
    epquery = query_by_condition_func("EasyPosts")
    message_dict = []
    rslist = ()

    time_format = "%Y-%m-%d"
    today = datetime.now()

    if time_range == "recent":
        frontday = today - timedelta(7)
        rslist = epquery(["postPublishTime"], [3], [time.strftime(time_format, frontday.timetuple())])
    elif time_range == "earlier":
        startday = today - timedelta(15)
        endday = today - timedelta(7)
        rslist = epquery(["postPublishTime","postPublishTime"],
            [2,3],
            [time.strftime(time_format, endday.timetuple()), time.strftime(time_format, startday.timetuple())])
    elif time_range == "old":
        startday = today - timedelta(30)
        endday = today - timedelta(15)
        rslist = epquery(["postPublishTime","postPublishTime"],
            [2,3],
            [time.strftime(time_format, endday.timetuple()), time.strftime(time_format, startday.timetuple())])
    else:
        return message_dict
    
    for rs in rslist:
        news_id = rs[1]
        news_title = rs[2]
        news_date = rs[3]
        news_has_img = rs[6]
        news_img_name = rs[8]

        if not news_has_img:
            news_img_name = "logo.png"
        
        date_format = "%Y-%m-%d"

        message_dict.append({
            "news_id" : news_id,
            "detailed_url" : news_id,
            "publish_date": time.strftime(date_format, news_date.timetuple()),
            "news_title": news_title,
            "news_img_name": news_img_name,
        })

    # 最后给message_dict排序，日期后的在前面
    def choose_date(news_dict):
        return news_dict["publish_date"]

    message_dict.sort(key = choose_date, reverse = True)

    return message_dict