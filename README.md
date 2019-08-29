# nhkspider

## 项目说明
python3 爬虫项目，主要是爬取`NHK news`(目前是`easy news`)。目的是方便看NHKnews吧，虽然相关的app也有，但是有时会墙。然后可以将本项目部署到没有被墙的服务器上加定时爬取、推送的功能，方便查看新闻。

- [x] Version(1.0) 爬取的对象是news和news里面提及的单词注解。  
- [x] Version(1.1) 将把news的汉字假名注释加进去的。  
- [x] Version(1.2.1) 将加入详情页的语音。
- [ ] Version(1.2.2) 将加入详情页的视频。  

技术栈：
+ 数据库: mysql + pymysql
+ 数据爬取: requests + BeautifulSoup
  + .m3u8视频解析： ffmpeg
+ 展示网页: Jquery(ajax) + flask

python 相关库
+ flask
+ pycrypto / pycryptodomex
+ pymysql
+ requests
+ bs4


## 工程结构
本项目包含两个工程：
1. 爬虫：可以使用`linux`的`crontab`服务配置定时启动，主程序入口是`start.py`，并且还包含一个简单的`log`脚本`auto-crawl.sh`，该脚本将爬取时的记录写入当日时间命名的项目的log文件夹的log文件中，如有错误将写入一个`error.log`中。

   ```bash
   sudo chmod +x 'auto-crawl.sh'
   ./auto-crawl.sh #启动一次爬取
   ```

2. 展示网页：后端使用`flask`，前端依赖`ajax`去后台拉取数据，尽量把后端做成接口式的，将前后端完全分离。`flask`程序主入口是`nhkboard.py`文件。