# -*- coding:utf8 -*-

'''
    @Author: Victor Chen
    @File  :  route3.py
    @Description:
        爬取历史top-list的文章
'''

import os,sys
sys.path.append(os.path.abspath(os.curdir))

import random
import time

import requests
from bs4 import BeautifulSoup

from entity.EasyNewsT import EasyNews
from entity.DangoMean import DangoMean

from service import EasyNewsStoreService1 as storeService

from spider.spider_util import getRandomHeaders
from spider.route2 import download_files,inforParser,dicParser,download_audio

# urls
main_url = "https://www3.nhk.or.jp/news/easy/"
main_news_json_url = "https://www3.nhk.or.jp/news/easy/top-list.json"
side_news_json_url = "https://www3.nhk.or.jp/news/easy/news-list.json"
base_img_url = "https://www3.nhk.or.jp/news/html/"

# formats
timeformat = "%Y-%m-%d %H:%M:%S"
dateformat = "%Y%m%d"

# path
project_path = os.path.abspath(os.curdir)


def scrapeHistory(url = side_news_json_url):

    print("Starting filling the history news...")
    # 
    rep = requests.get(url, headers = getRandomHeaders())
    mjson = rep.json()[0]

    # 以时间为key, value是每个日期内的新闻，包含五条左右，每条新闻是一个dict字典类型
    # 每条新闻的dict的key,value 和 一致。


    for news_date, news_list in mjson.items():

        newsInfo = []
        # 每天的news
        print("Scrape easy news in date'{}'".format(news_date))

        for thatnews in news_list:
            news = EasyNews()

            news.news_id = thatnews["news_id"]
            news.title = thatnews["title"]
            news.publish_time = thatnews["news_prearranged_time"]
            news.has_img = thatnews["has_news_web_image"]
            news.has_audio = thatnews["has_news_web_movie"]

            # 下载图片
            if news.has_img:
                basic_url = thatnews["news_web_image_uri"]
                relpath = "/".join(basic_url.split("/")[-2:])
                img_ext = relpath.split(".")[-1]
                img_url = base_img_url + relpath


                # date + news_id 作为图片名字
                time_tuple = time.strptime(news.publish_time, timeformat)
                date_str = time.strftime(dateformat, time_tuple)
                name = "{}_{}.{}".format(date_str, news.news_id, img_ext)
                news.img_name = name

                # 下载 
                download_files(img_url, news.img_base_path, name)

            if news.has_audio:
                name = "{}_{}.mp4".format(date_str, news.news_id)
                news.audio_name = name

                download_audio(
                    news.news_id,
                    project_path + news.audio_base_path,
                    name
                )     

            newsInfo.append(news)
            # infrom
            print("Exract news:%s" %(news.title)) 

        # 以date为单位爬取每一天的新闻的详情页
        for news in newsInfo:
            mainId = news.news_id
            
            # 详情页的爬取
            url = "https://www3.nhk.or.jp/news/easy/%s/%s.html" %(mainId, mainId)
            resp = requests.get(url, headers = getRandomHeaders())
            inforParser(resp, news)

            # 详情页的dic字典的爬取
            url = "https://www3.nhk.or.jp/news/easy/%s/%s.out.dic" %(mainId, mainId)
            resp = requests.get(url, headers = getRandomHeaders())
            dics = dicParser(resp)
            print("Parsed detailed news:%s" %(news.title))

            # 单个news存储
            storeService.store_one_news(news,dics)
            print("Stored")

            # 随机暂停
            time.sleep(random.random())