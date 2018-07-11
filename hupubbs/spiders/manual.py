# -*- coding: utf-8 -*-
import socket
import datetime
import scrapy
from hupubbs.items import HupubbsItem, HupubbsSubjectItem
from scrapy.loader import ItemLoader
from scrapy.http import Request
from urllib import parse


class BasicSpider(scrapy.Spider):
    name = 'manual'
    allowed_domains = ['bbs.hupu.com']
    start_urls = ['https://bbs.hupu.com/china-soccer']

    def parse(self, response):
        protocol, url_no_protocol = parse.splittype(response.url)
        host, url_no_host = parse.splithost(url_no_protocol)
        # Other page URLS
        for i in range(10):
            if i > 0:
                yield Request("%s-%d"%(response.url, i + 1), callback=self.parse)
        # Get subject URLs and yield Requests
        subject_selector = response.xpath('//*[@class="truetit"]/@href')
        for url in subject_selector.extract():
            yield Request(parse.urljoin(protocol + "://" + host,url), callback=self.parse_item)

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
