# -*- coding: utf-8 -*-
import scrapy
from hupubbs.items import HupubbsItem

class BasicSpider(scrapy.Spider):
    name = 'basic'
    allowed_domains = ['web']
    start_urls = ['https://bbs.hupu.com/china-soccer']

    def parse(self, response):
        item = HupubbsItem()
        item['forum_name'] = response.xpath('//*[@id="forumname"]/text()').extract()[0]
        item['total_theme_count'] = response.xpath('//*[@class="pageright"]/text()').re('[0-9]+')[0]
        item['total_reply_count'] = response.xpath('//*[@class="pageright"]/text()').re('[0-9]+')[1]
        item['today_post_count'] = response.xpath('//*[@class="pageright"]/text()').re('[0-9]+')[2]
        return item
