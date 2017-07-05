# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem
import scrapy
import re
from .settings import MONGO_URI,MONGO_DB

class MeizituPipeline(ImagesPipeline):
    client = pymongo.MongoClient(MONGO_URI)
    db = client[MONGO_DB]
    table = db['meizitu']

    def file_path(self, request, response=None, info=None):
        item = request.meta['item']
        folder = item['name']
        folder_strip = MeizituPipeline.strip(folder)
        image_guid = request.url.split('/')[-1]
        month = request.url.split('/')[-2]
        year = request.url.split('/')[-3]
        filename = u'{0}/{1}/{2}/{3}'.format(year, month, folder_strip, image_guid)
        return filename

    def get_media_requests(self, item, info):
        isnot = self.table.find_one({'name':item['name']})
        if not isnot:
            for img_url in item['img_urls']:
                yield scrapy.Request(img_url,meta={'item':item})

    def item_completed(self, results, item, info):
        img_paths = [x['path'] for ok, x in results if ok]
        if not img_paths:
            raise DropItem('Item contains no images')
        return item

    @staticmethod
    def strip(path):
        path = re.sub(r'[？\\*|“<>:/]','',str(path))
        return path


    # def process_item(self, item, spider):
    #     return item

class save_mongodb(object):
    def __init__(self, mongo_db, mongo_uri):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls,crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DB')
        )

    def open_spider(self,spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self,spider):
        self.client.close()

    def process_item(self, item, spider):
        self.db['meizitu'].update({'name':item['name']},{'$set':item},True)
        return item

