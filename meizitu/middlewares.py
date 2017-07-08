# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html
from meizitu.agents import agents
from scrapy import signals
from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware
import random
import redis
import logging

logger = logging.getLogger(__name__)

class MeizituSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)

class RandomUserAgent(UserAgentMiddleware):

    def process_request(self, request, spider):
        agent = random.choice(agents)
        request.headers['User-Agent'] = agent


class Myproxymiddleware(object):

    def __init__(self,redis_host,redis_port,redis_password,redis_proxypool_name):
        self.proxypool_name = redis_proxypool_name
        if redis_password:
            self.client = redis.Redis(redis_host,redis_port,1,redis_password)
        else:
            self.client = redis.Redis(redis_host, redis_port, 1)
        self.proxy = self._get_proxy()
        self.count = 0

    @classmethod
    def from_crawler(cls,crawler):
        return cls(
            redis_host = crawler.settings.get('REDIS_HOST'),
            redis_port = crawler.settings.get('REDIS_PORT'),
            redis_password = crawler.settings.get('REDIS_PASSWORD'),
            redis_proxypool_name=crawler.settings.get('REDIS_PROXYPOOL_NAME')
        )

    def _get_proxy(self):
        try:
            return self.client.rpop(self.proxypool_name).decode('utf-8')
        except:
            logger.warning('代理池为空')

    def _put_back(self,proxy):
        self.client.lpush(self.proxypool_name, proxy)

    def process_request(self,request,spider):
        """将代理添加到request中"""
        # 如何有设置不使用代理，则退出返回
        if 'dont_proxy' in request.meta.keys():
            return
        # 如果代理池为空，则退出返回
        if not self.proxy:
            return
        request.meta['proxy'] = 'http://'+self.proxy
        self.count += 1

    def process_response(self, request, response, spider):
        """检查response，根据返回码切换proxy"""
        if response.status != 200:
            now_proxy = request.meta['proxy']
            if self.proxy in now_proxy:
                logger.info('%s 被BAN或错误，共爬取%s网页' %(now_proxy,self.count))
                self.proxy = self._get_proxy()
                self.count = 0
                # if hasattr(spider,'httpstatus_allow_list') and response.status in spider.httpstatus_allow_list:
                self._put_back(now_proxy)
            new_request = request.copy()
            # 将新请求取消默认的URL去重
            new_request.dont_filter = True
            return new_request
        else:
            return response

    def process_exception(self, request, exception, spider):
        now_proxy = request.meta['proxy']
        # logger.error('蜘蛛 %s 发生错误:%s ,错误的请求为：%s ,代理为：%s' % (spider, exception, request, now_proxy))
        if self.proxy in now_proxy:
            logger.info('%s 连接超时，共爬取%s网页' % (now_proxy, self.count))
            self.proxy = self._get_proxy()
            self.count = 0
        new_request = request.copy()
        new_request.dont_filter = True
        return new_request





