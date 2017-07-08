# -*- coding: utf-8 -*-
import scrapy
from meizitu.items import MeizituItem

class MeiziSpider(scrapy.Spider):
    name = "meizi"
    url = 'http://www.mzitu.com/all/'
    httpstatus_allow_list = [514]

    def start_requests(self):
        yield scrapy.Request(self.url, callback=self.next_url)

    def next_url(self, response):
        img_years = response.css('.all .archives')
        for year in range(3):
            img_group = img_years[year].css('li p.url a::attr(href)').extract()
            for img in img_group:
                yield scrapy.Request(img,callback=self.parse_img)

    def parse_img(self,response):
        item = MeizituItem()
        name = response.css('.content .main-title::text').extract_first()
        img_firstpage = response.css('.content .main-image p a img::attr(src)').extract_first()
        max_page = int(response.css('.content .pagenavi a span::text').extract()[-2])
        img_urls = []
        pages = ['0' + str(x) if len(str(x)) == 1 else str(x) for x in range(1, max_page + 1)]
        for page in pages:
            img_url = img_firstpage[:-6] + page + img_firstpage[-4:]
            img_urls.append(img_url)
        item['name'] = name
        item['img_urls'] = img_urls
        return item

