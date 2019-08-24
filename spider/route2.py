# -*- coding:utf8 -*-

'''
    @Author: Victor Chen
    @File  :  route.py
    @Description:
        爬取 + parser + 持久化主函数
'''

import os,sys
sys.path.append(os.path.abspath(os.curdir))

import random
import time
import threading

import requests
from bs4 import BeautifulSoup

from entity.EasyNewsT import EasyNews
from entity.DangoMean import DangoMean

from service import EasyNewsStoreService1 as storeService
from spider.spider_util import getRandomHeaders,encodeUTF8
from spider.audio_spider import retrieve_audio

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

# 处理详情页的信息
def inforParser(response, entity):

    if response.status_code != 200:
        print("%s response %d" %(response.url, response.status_code))

    html = response.text
    if response.encoding != 'UTF-8':
        html = response.content.decode('utf-8')

    # parser
    soup = BeautifulSoup(html, "html.parser")
    mcontent = soup.find_all('div', attrs={"id":"js-article-body"})[0]
    paragraphs = mcontent.find_all("p")

    str_content = ""
    for paragraph in paragraphs:

        # 去除span标签和a标签，保留原有文字的ruby注音
        while paragraph.a != None:
            paragraph.a.unwrap()

        while paragraph.span != None:
            paragraph.span.unwrap()

        # 转化为字符串
        content_with_ruby = ''.join([str(p) for p in paragraph.contents])
        str_content += content_with_ruby + "\n"
        pass

    entity.content = str_content
    pass


# 字典页面的爬取
def dicParser(response):

    rjson = response.json()
    dics = rjson["reikai"]["entries"]

    respEncode = response.encoding

    descwords = []
    for _, dicdesc in dics.items():
        
        # 一个词可能对应多个解释所以hash也不唯一?
        for definitions in dicdesc:
            words = DangoMean()

            # 不确定是否存在多个hyouki的情况，这里先简单处理
            if len(definitions["hyouki"]) != 1:
                print("Mulitiple hyouki of %s: %d" %(defs, len(definitions["hyouki"])))
            
            # 转化编码
            defs = encodeUTF8(definitions["def"], respEncode)
            hyoukis = encodeUTF8(definitions["hyouki"][0], respEncode)

            # 再用bs4 处理下
            defsparser = BeautifulSoup(defs, "html.parser")
            for tag in defsparser.find_all("rt"):
                tag.clear()

            words.dango = hyoukis
            words.mean = defsparser.getText()
            words.generate_hash()

            descwords.append(words)

    return descwords


# 下载二进制文件并保存
def download_files(url, basepath, name):
    try:

        files = requests.get(url, headers=getRandomHeaders())
        files = files.content

        fpath = project_path + os.sep + basepath
        if not os.path.exists(fpath):
            os.makedirs(fpath)

        with open(fpath + os.sep + name, "wb") as f:
            f.write(files)

    except Exception as ex:
        print("error: {}".format(ex))

# 
def download_audio(news_id, basepath, name):
    try:
        if not os.path.exists(basepath):
            os.makedirs(basepath)
        if name not in os.listdir(basepath):
            
            class audioThread(threading.Thread):
                def __init__(self):
                    threading.Thread.__init__(self)

                def run(self):
                    print("Begin downloading audio file.")
                    retrieve_audio(
                        news_id = news_id, 
                        base_audio_file_path = basepath,
                        mp4_filename= name)

            athread = audioThread()
            athread.start()
        else:
            print("Audio already exists.")

    except Exception as ex:
        pass

# 处理主页的信息
def scrapeMain(url = main_url):

    print("starting .. ")
    # request the json
    mjsons = requests.get(main_news_json_url, headers=getRandomHeaders())
    mjsons = mjsons.json()

    print(len(mjsons))

    newsInfo = []

    for mjson in mjsons:
        news = EasyNews()

        news.news_id = mjson["news_id"]
        news.title = mjson["title"]
        news.publish_time = mjson["news_prearranged_time"]
        news.has_img = mjson["has_news_web_image"]
        news.has_audio = mjson["has_news_web_movie"]

        # 获取时间
        time_tuple = time.strptime(news.publish_time, timeformat)
        date_str = time.strftime(dateformat, time_tuple)

        # 下载图片
        if news.has_img:
            basic_url = mjson["news_web_image_uri"]
            relpath = "/".join(basic_url.split("/")[-2:])
            img_ext = relpath.split(".")[-1]
            img_url = base_img_url + relpath


            # date + news_id 作为图片名字
            name = "{}_{}.{}".format(date_str, news.news_id, img_ext)
            news.img_name = name

            # 下载 
            download_files(img_url, news.img_base_path, name)

        # 下载音频只需要提供easynews的news_id，保存路径和文件名
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

    # 对每一个首页的新闻进一步获取详细的其他信息
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

    pass