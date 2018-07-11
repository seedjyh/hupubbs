# -*- coding: utf-8 -*-
import scrapy
import socket
import datetime
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.loader import ItemLoader
from hupubbs.items import HupubbsSubjectItem

class EasySpider(CrawlSpider):
    name = 'easy'
    allowed_domains = ['bbs.hupu.com']
    start_urls = ['https://bbs.hupu.com/china-soccer']

    rules = (
        Rule(LinkExtractor(restrict_xpaths='//*[@class="truetit"]'), callback='parse_item'),
    )

    def parse_item(self, response):
        """
        @url https://bbs.hupu.com/china-soccer
        @returns items 1
        @scrapes title poster_user_url poster_nickname
        @scrapes url project spider server date
        :param response: 
        :return: 
        """
        l = ItemLoader(item=HupubbsSubjectItem(), response=response)
        l.add_xpath('title', '//h1[@id="j_data"]/text()')
        l.add_xpath('poster_user_url', '//div[@id="tpc"]//a[@class="u"]/@href')
        l.add_xpath('poster_nickname', '//div[@id="tpc"]//a[@class="u"]/text()')
        l.add_value('url', response.url)
        l.add_value('project', self.settings.get('BOT_NAME'))
        l.add_value('spider', self.name)
        l.add_value('server', socket.gethostname())
        l.add_value('date', datetime.datetime.now())
        return l.load_item()
