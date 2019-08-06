# nhkspider

## 项目说明
***
爬虫项目，主要是爬取`NHK news`(目前是`easy news`)。目的是方便看NHKnews吧，虽然相关的app也有，但是有时会墙。然后可以将本项目部署到没有被墙的服务器上加定时爬取、推送的功能，方便查看新闻。

Version(1.0) 爬取的对象是news和news里面提及的单词注解。
Version(1.1) 将把news的汉字假名注释加进去的。

技术栈：
+ 数据库：mysql + pymysql
+ 数据爬取： requests + BeautifulSoup

数据库设计的超混乱的现在，我会改的！