# -*- coding:utf8 -*-

'''
    @Author: Victor Chen
    @File  :  DescWords.py
    @Description:
        对应单词的注解的实体类
'''

import hashlib

class DescWords(object):
    def __init__(self):
        super().__init__()
        self.preSetAttr = ["wordsMain","wordsDesc"]
        self.wordsMain = ""
        self.wordsDesc = ""
        # self._setHash()
    
    def setAttribute(self, *args, **kws):

        for key, value in kws.items():
            if key not in self.preSetAttr:
                continue
            if self.preSetAttr.index(key) == 0:
                self.wordsMain = value
            elif self.preSetAttr.index(key) == 1:
                self.wordsDesc = value

        # update the hash value
        # self._setHash()

        pass

    def __str__(self):
        desc = "words:{};wordsHash:{};".format(
            self.wordsMain,
            self.wordsDesc,
        )
        return desc