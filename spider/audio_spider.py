# -*- coding:utf8 -*-

'''
    @Author: Victor Chen
    @File  :  audio_spider.py
    @Description:
        用于爬取audio的spider，主要是根据easynews的
'''

import requests
import os, sys
from Crypto.Cipher import AES
import threading
import time

from spider.spider_util import getRandomHeaders, mulithread_download

def pad(text):
    while len(text) % 16 != 0:
        text += b' '    
    return text

def pad_key(key):
    while len(key) % 16 != 0:
        key += b' '
    return key


def download_and_decrypt(decrypt_obj, uri, base_path, filename, max_retry_times = 5):
    """下载资源并解密保存在 `base_path + filename` 文件中"""
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
                raise Exception("HttpError: Request for {} overwhelm the max retry times:{}".format(uri, max_retry_times))
        except Exception as ex:
            raise(ex)

    resp_bytes = resp.content

    with open(base_path+filename, "wb") as segf:
        segf.write(decrypt_obj.decrypt(pad(resp_bytes)))

    print("Save resource in {} succeeded.".format(base_path + filename))


def retrieve_audio(news_id, base_audio_file_path, mp4_filename = ""):
    """ 下载某一个easynews的音频：解析对应的m3u8文件，爬取ts文件再解密合成.mp4文件 """
    main_m3u8_name = "master.m3u8"
    main_m3u8_path = "https://nhks-vh.akamaihd.net/i/news/easy/{}.mp4/".format(news_id)
    main_m3u8_url = main_m3u8_path + main_m3u8_name

    print("parsing m3u8 file: \'{}\'".format(main_m3u8_name))
    # the first m3u8
    main_m3u8 = requests.get(main_m3u8_url, headers=getRandomHeaders()).text

    for line in main_m3u8.split("\n"):
        if "#EXT" in line:
            continue
        elif "http" in line:
            next_link = line

    # use next_link get the next m3u8
    print("parsing m3u8 file: \'{}\'".format(next_link))
    next_m3u8 = requests.get(next_link, headers=getRandomHeaders()).text
    next_m3u8_lines = next_m3u8.split("\n")
    
    next_m3u8_lines[0] == "#EXTM3U"

    segments = {}
    for i in list(range(len(next_m3u8_lines))):
        line = next_m3u8_lines[i]
        
        # get keys
        if "#EXT-X-KEY" in line:
            params = line[line.find(":")+1:].replace("\"", "").replace("\'", "")
            param_list = params.split(",")
            keys_param = {}
            for param in param_list:
                indx = param.find("=")
                if indx == -1:
                    raise Exception("parse key value:\'{}\' error".format(param))
                keys_param[param[:indx]] = param[indx+1:]

        # get url list:
        if "#EXTINF" in line:
            i += 1
            uri = next_m3u8_lines[i]
            try:
                segment_length = line[line.find(':')+1:-1]
                segment_length = float(segment_length)

                segment_name = uri.split("?")[0].split("/")[-1]
                segment_index = segment_name.split(".")[0].split("_")[0][7:]
                # print("parser No.{} segment".format(segment_index))

                # append
                segments[segment_index] = [
                    segment_name,
                    segment_length,
                    uri
                ]

            except Exception as ex:
                print("Parser Error in line:{}".format(i-1))
                raise(ex)
    
    # decipher and get .ts files
    ts_file_paths = []
    base_tmpfile_path = os.sep.join([
        "templates","downloaded","audio","tmp"
    ]) + os.sep
 
    if not os.path.exists(base_tmpfile_path):
        os.makedirs(base_tmpfile_path)

    print("parsing and scraping temp audios...")
    # grep and save keys
    key = requests.get(keys_param["URI"], headers=getRandomHeaders()).content
    # m3u8 use AES128 and CBC mode as default
    aes = AES.new(pad_key(key), AES.MODE_CBC, b"0000000000000000")

    uris = []
    filenames = []
    # scrape the ts audio
    for ind, vals in segments.items():
        name, length, uri = vals
        uris.append(uri)
        filenames.append("{}_{}".format(news_id, name))

    # use multithreads to download resources
    mulithread_download(
        uris, base_tmpfile_path, filenames, 
        donwload_func=download_and_decrypt, decrypt_obj=aes)

    ts_file_paths = [base_tmpfile_path + filename for filename in filenames]

    print("Combine the .ts audio....")
    # use ffmpeg to combine all the file up into one mp4 file
    # construct command args

    if not os.path.exists(base_audio_file_path):
        os.makedirs(base_audio_file_path)
    if mp4_filename == "":
        mp4_path = base_audio_file_path + "{}".format(news_id)
    else:
        mp4_path = base_audio_file_path + "{}".format(mp4_filename)
    input_file_str = " \"concat:{}\" ".format("|".join(ts_file_paths))

    # run ffmpeg
    ffmpeg_command = " ".join(["ffmpeg","-i", input_file_str, "-c","copy", mp4_path])
    returnObj = os.system(ffmpeg_command)
    if returnObj != 0:
        raise Exception("Command execution failed.")
    print("Combined ts into {}".format(mp4_path))

    for ts_file_path in ts_file_paths:
        os.remove(ts_file_path)

    pass
