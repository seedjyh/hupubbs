# -*- coding: utf-8 -*-
import scrapy


class BasicSpider(scrapy.Spider):
    name = 'basic'
    allowed_domains = ['web']
    start_urls = ['https://bbs.hupu.com/china-soccer']

    def parse(self, response):
        self.log("title: %s" % response.xpath('//*[@id="forumname"]/text()').extract()[0])
        self.log("total_theme_count: %d" % int(response.xpath('//*[@class="pageright"]/text()').re('[0-9]+')[0]))
        self.log("total_reply_count: %d" % int(response.xpath('//*[@class="pageright"]/text()').re('[0-9]+')[1]))
        self.log("today_post_count: %d" % int(response.xpath('//*[@class="pageright"]/text()').re('[0-9]+')[2]))
        pass
