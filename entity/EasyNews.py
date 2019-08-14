# -*- coding:utf8 -*-

'''
    @Author: Victor Chen
    @File  :  EasyNews.py
    @Description:
        EasyNews 实体类
'''

import datetime

class EasyNews(object):
    def __init__(self):
        super().__init__()
        self.preSetAttr = ["title","publishTime","newsId","content"]
        self.id = 0
        self.title = ""
        self.publishTime = ""
        self.newsId = ""
        self.content = ""

    def set(self, *args, **kws):
        """ attribute: ['id', title','publishTime','newsId','content'] """
        for key,value in kws.items():
            if key not in self.preSetAttr:
                continue
            if self.preSetAttr.index(key) == 0:
                self.title = value
            elif self.preSetAttr.index(key) == 1:
                self.publishTime = value
            elif self.preSetAttr.index(key) == 2:
                self.newsId = value
            elif self.preSetAttr.index(key) == 3:
                self.content = value

    def __str__(self):
        return "[newsId:{};title:{};publishTime:{};content:{};]".format(
            self.newsId,
            self.title, 
            self.publishTime,
            self.content)