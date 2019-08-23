# -*- coding:utf8 -*-

'''
    @Author: Victor Chen
    @File  :  run.py
    @Description:
        flask 主程序

'''

import os,sys
import json

from entity.EasyNewsT import EasyNews

from flask import Flask
from flask import render_template,url_for

from service.EasyNewsRenderService import *

app = Flask(__name__)

def process_url(news):
    # 处理图片和音频的路径
    tmp = EasyNews()
    img_save_relpath = tmp.img_base_path
    audio_save_relpath = tmp.audio_base_path

    news["img_url"] = img_save_relpath + news["news_img_name"]
    if news["news_has_audio"]:
        news["audio_url"] = audio_save_relpath + news["news_audio_name"]


@app.route("/easynews/show/index")
def render_index():
    print("get requests")

    # 返回之前将查询的数据进行修改，做路径拼接
    rj =  render_index_time_range_json("recent")
    for news in rj:
        process_url(news)

    return json.dumps(rj)


@app.route("/easynews/show/index/<news_time_range>")
def render_date_range_index(news_time_range):
    print(news_time_range)

    # 返回之前将查询的数据进行修改，做路径拼接
    rj =  render_index_time_range_json(news_time_range)
    for news in rj:
        process_url(news)

    return json.dumps(rj)


@app.route("/easynews/show/detailedcontent/<news_id>")
def render_detailed_json(news_id):

    print("render news:{} 's detailed content".format(news_id))
    news = render_detailed_content(news_id)

    # 如果没查到那么返回空
    if len(news.keys()) == 0:
        return json.dumps(news)

    # 1. 修改查询数据
    process_url(news)

    return json.dumps(news)


@app.route("/")
def render_index_html():
    print(url_for("static",filename = "index.css"))
    return render_template("index.html")


@app.route("/detailed/<news_id>")
def render_detailed_html(news_id):
    return render_template("detailed.html")


@app.route("/error/<int:error_code>")
def render_error_page(error_code):
    if error_code == 404:
        return render_template("error.html", message = "Your requests page is misssing.")

    else:
        print(error_code)
        return render_template("error.html", message="Unkown error occured.")


if __name__ == "__main__":
    app.run(host='0.0.0.0')