# -*- coding:utf8 -*-

'''
    @Author: Victor Chen
    @File  :  spider_util.py
    @Description:
        用于spider的一些函数
'''

import os,sys
import requests
import random
import threading
import time
import queue


# backup headers parameters
user_agents = [
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36",
    "Mozilla/5.0 (Linux; U; Android 4.0.3; ko-kr; LG-L160L Build/IML74K) AppleWebkit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30",
    "Mozilla/5.0 (Linux; U; Android 4.0.4; en-gb; GT-I9300 Build/IMM76D) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30",
    "Mozilla/5.0 (Linux; Android 4.0.4; Galaxy Nexus Build/IMM76B) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.133 Mobile Safari/535.19",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.11 (KHTML, like Gecko) Ubuntu/11.10 Chromium/27.0.1453.93 Chrome/27.0.1453.93 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 6_1_4 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) CriOS/27.0.1453.10 Mobile/10B350 Safari/8536.25",
    "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_6; en-US) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.4 Safari/533.20.27",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 5_0 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko) Version/5.1 Mobile/9A334 Safari/7534.48.3",
    "Mozilla/5.0 (iPad; CPU OS 5_0 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko) Version/5.1 Mobile/9A334 Safari/7534.48.3"
]

# 生成随机的headers
def getRandomHeaders():
    headers = {}
    random_user_agent = user_agents[random.randint(0, len(user_agents)-1) ]
    headers['user-agent'] = random_user_agent
    return headers


# 转化编码格式
def encodeUTF8(string, orginal_encode):
    return string.encode(orginal_encode).decode("utf-8")


def download_resource(uri, base_path, filename, max_retry_times = 5):
    """下载资源并保存在 `base_path + filename` 文件中"""
    # 设置重传
    retry_time = 0

    resp = None
    while not isinstance(resp, requests.Response):
        try:
            resp = requests.get(uri, headers=getRandomHeaders())
        except requests.exceptions.SSLError:
            resp = ""
            retry_time = retry_time + 1
            print("Retry request for {} at No.{} time".format(uri, retry_time))
            if (retry_time == max_retry_times):
                raise Exception("HttpError: Request for {} exceed the max retry times:{}".format(uri, max_retry_times))
        except Exception as ex:
            raise(ex)

    resp_bytes = resp.content

    with open(base_path+filename, "wb") as rwf:
        rwf.write(resp_bytes)

    print("Save resource in {} succeeded.".format(base_path + filename))


def mulithread_download(uri_list, base_paths, filenames, max_thread_num = 5, donwload_func=download_resource, *args, **kws):
    """ 多线程下载资源 
    
    params:
        uri_list        (list)  对应资源的uri
        base_paths      (list)  对应资源要存储的路径，指定base_paths为字符串时，所有资源的路径相同
        filenames       (list)  对应资源的保存文件名
        max_thread_num  (int)   最多使用的线程数
        download_func   (func)  单个线程使用的下载的方法
    """
    # thread`s class for downloading
    class _download_threads(threading.Thread):
        def __init__(self, res_info_dict):
            threading.Thread.__init__(self)
            self.res_info_dict = res_info_dict

        def run(self):
            donwload_func(
                *args,
                uri = self.res_info_dict["uri"],
                base_path = self.res_info_dict["base_path"],
                filename = self.res_info_dict["filename"],
                **kws
            )

    # construct dict
    if isinstance(base_paths, str):
        base_paths = [base_paths for i in range(len(uri_list))]

    res_infos = [
        {
            "uri": uri,
            "base_path": base_path,
            "filename": filename
        } for uri, base_path, filename in zip(uri_list, base_paths, filenames) 
    ]

    info_queue = queue.Queue()
    for res_info in res_infos:
        info_queue.put(res_info)

    thread_list = []
    while not info_queue.empty():

        while not info_queue.empty() and len(thread_list) < max_thread_num:
            res_info = info_queue.get()
            tmp_thread = _download_threads(res_info)
            tmp_thread.start()
            thread_list.append(tmp_thread)
        
        # check thread in thread_list
        rm_list = []
        for th in thread_list:
            if th.is_alive():
                th.join()
            else:
                rm_list.append(th)

        # remove 
        for rm_thread in rm_list:
            thread_list.remove(rm_thread)

        # time.sleep(random.random())

    print("download completed.")
    pass