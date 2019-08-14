# -*- coding:utf8 -*-

'''
    @Author: Victor Chen
    @File  :  EasyNewsT.py
    @Description:
        升级版的EasyNews 实体类
'''

"""
EasyNews 应该具有的属性有:
    id, newsid, type, title, publish_time, content, 
    img, audio,  ( img 和 audio 应该保存的是img和audio的唯一名称)
    dangos ( 包含的单词组 ) ( 需要和其他的表一起联合查询 )

    应该具有的方法：
        (1) 每个属性对应的get/set方法
"""

import os

class EasyNews:
    def __init__(self):
        self.id = 0
        self.news_id = ""
        self.type = 1
        self.title = ""
        self.publish_time = ""
        self.content = ""
        self.img_name = ""
        self.audio_name = ""
        self.has_img = False
        self.has_audio = False
        self.dangos = []

        self.img_base_path = os.sep.join(["", "static", "downloaded" ,"easyNews", "img",""])
        self.audio_base_path = os.sep.join(["", "static", "downloaded", "easyNews", "audio",""])

    def __str__(self):
        s = "[news_id:{},title:{}]".format(self.news_id, self.title)
        return s

    def get_dict(self):
        """ return all self parameters as a dict """
        para_dict = {
            "id": self.id,
            "news_id": self.news_id,
            "type": self.type,
            "title": self.title,
            "publish_time": self.publish_time,
            "content": self.content,
            "img_name": self.img_name,
            "audio_name": self.audio_name,
            "has_img": self.has_img,
            "has_audio": self.has_audio,
            "dangos": self.dangos
        }

        return para_dict
