
# MEIZITU
> 抓取 www.mzitu.com 网站中2015年至今的所有图片，下载图片保存到本地，并将url等信息保存到mongodb数据库

**PS: 此网站已经的图片下载已经做了修改，已无法直接爬取，此项目已失效。不提供长期支持，只供学习参考，有兴趣的朋友可自行研究**

<br>

## 使用：
##### 自定义图片保存路径

在`settings`文件中进行配置
```
IMAGES_STORE = 'F:\Girls-Images\\'
```

<br>

##### 选择是否启用代理池
> PS: 内置了代理中间件，代理中间件中利用了我之前的一个维护免费代理池项目 项目名：Myproxypool
> 若要使用，需要进行此项目，安装此项目
> 不使用的话请在`settings`中注释掉此配置项

默认是注释掉的
    
    # 'meizitu.middlewares.Myproxymiddleware':752
    
<br>

##### 启动
在项目根目录运行以下命令
```angular2html
scrapy crawl meizi
```
