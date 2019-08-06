# -*- coding:utf8 -*-

'''
    @Author: Victor Chen
    @File  :  configuration.py
    @Description:
        读取配置信息
'''

import json
import os

from utils.mode import Singleton

# 项目全局配置类，行为是单例模式
@Singleton
class pconfig:
    def __init__(self, level = "normal"):
        self.inconfig = None
        self._load_config(level)

    def _load_config(self, level):
        file_base_path = os.path.abspath(os.curdir) + os.sep + "config" + os.sep
        if level == "normal":
            with open(file_base_path+"normal.json", "r") as fp:
                self.inconfig = json.load(fp)

    def change_level(self, level):
        self._load_config(level)

    def get_config(self):
        return self.inconfig
