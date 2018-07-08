# -*- coding: utf-8 -*-
import scrapy
from hupubbs.items import HupubbsItem
from scrapy.loader import ItemLoader


class BasicSpider(scrapy.Spider):
    name = 'basic'
    allowed_domains = ['web']
    start_urls = ['https://bbs.hupu.com/china-soccer']

    def parse(self, response):
        l = ItemLoader(item=HupubbsItem(), response=response)
        l.add_xpath('forum_name', '//*[@id="forumname"][1]/text()')
        l.add_xpath('total_theme_count', '//*[@class="pageright"]/text()', re='共([0-9]+)主题')
        l.add_xpath('total_reply_count', '//*[@class="pageright"]/text()', re='/([0-9]+)回复')
        l.add_xpath('today_post_count', '//*[@class="pageright"]/text()', re='今日([0-9]+)帖')
        return l.load_item()
