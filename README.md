
MEIZITU
抓取 www.mzitu.com 网站中2015年至今的所有图片，下载图片保存到本地，并将url等信息保存到mongodb数据库
内置了代理中间件和随机替还User-Agent的中间件，代理中间件中利用了我之前的一个维护免费代理池项目 项目名：Myproxypool

使用方法（使用前先进行设置）：
使用前，先开启代理池，使用run.py开启代理池
然后正常使用 scrapy crawl spider 命名开启爬虫就OK了

设置：
打开 settings.py 文件进行设置，内有设置说明
