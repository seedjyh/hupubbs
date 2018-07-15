# -*- coding: utf-8 -*-
import scrapy
import re
from scrapy.http import Request
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from hupubbs.items import HupubbsUserItem, HupubbsThreadItem, HupubbsReplyItem

class ForumSpider(scrapy.Spider):
    name = 'forum'
    allowed_domains = ['hupu.com']
    start_urls = ['https://bbs.hupu.com/china-soccer']

    # 从论坛页的URL获取下一页的URL
    @staticmethod
    def next_forum_page_url(now_url):
        res = re.search("[0-9]+$", now_url)
        if res is None:
            return now_url + "-2"
        now_page_pos, _ = res.span()
        now_page_number = int(now_url[now_page_pos])
        now_url_base = now_url[:now_page_pos]
        return now_url_base + str(now_page_number + 1)

    # 从帖子页的URL获取下一页的URL
    @staticmethod
    def next_thread_page_url(now_url):
        res = re.search("^(.*\/[0-9]+)(-?)([0-9]*)(.html)$", now_url)
        if res is None:
            return now_url
        groups = res.groups()
        if groups[1] == "":
            return "%s-2%s" % (groups[0], groups[3])
        else:
            return "%s%s%d%s" % (groups[0], groups[1], int(groups[2]) + 1, groups[3])

    # 获取帖子页URL中的帖子ID
    @staticmethod
    def thread_id(url):
        res = re.search("^.*\/([0-9]+)(-?)([0-9]*)(.html)$", url)
        if res is None:
            return ""
        else:
            return res.groups()[0]

    # 爬虫入口，爬取一页并继续下一页
    def parse(self, response):
        # 横向：下一页
        yield Request(self.next_forum_page_url(response.url), self.parse)
        # 纵向
        le = LinkExtractor(restrict_xpaths='//a[@class="truetit"]')
        links = le.extract_links(response)
        for link in links:
            yield Request(link.url, callback=self.parse_thread)

    # 爬取单个帖子
    def parse_thread(self, response):
        # 横向：下一页
        yield Request(self.next_thread_page_url(response.url), self.parse)
        # 当页：顶楼
        selectors = response.xpath('//form/div[@id="tpc"]')
        for selector in selectors:
            for item in self.parse_subject(selector, response):
                yield item
        # 当页：高亮
        # selectors = response.xpath('//form/div[contains(@class, "w_reply")]//div[@class="floor"]')
        # 当页：所有回复
        selectors = response.xpath('//form/div[@id!="tpc"][@class = "floor"]')
        for selector in selectors:
            for item in self.parse_reply(selector, response):
                yield item

    # 解析顶楼
    def parse_subject(self, selector, response):
        # 解析发帖人
        user_item_loader = ItemLoader(item=HupubbsUserItem(), selector=selector)
        user_item_loader.add_xpath('forum_id', xpath='.//a[@class="u"]/@href', re='\/([0-9]+)$')
        user_item_loader.add_xpath('nickname', xpath='.//a[@class="u"]/text()')
        user_item_loader.add_xpath('signature', xpath='//div[@class="sign"]')
        yield user_item_loader.load_item()
        # 解析主题帖
        subject_item_loader = ItemLoader(item=HupubbsThreadItem(), selector=selector)
        subject_item_loader.add_value('forum_id', value=self.thread_id(response.url))
        subject_item_loader.add_xpath('user_forum_id', xpath='.//a[@class="u"]/@href', re='\/([0-9]+)$')
        subject_item_loader.add_xpath('post_time', xpath='.//span[@class="stime"]/text()')
        subject_item_loader.add_xpath('title', xpath='.//div[@class="subhead"]/span/text()')
        yield subject_item_loader.load_item()

    # 解析回帖
    def parse_reply(self, selector, response):
        # 解析回帖人
        user_item_loader = ItemLoader(item=HupubbsUserItem(), selector=selector)
        user_item_loader.add_xpath('forum_id', xpath='.//div[@class="left"]/a[@class="u"]/@href', re='\/([0-9]+)$')
        user_item_loader.add_xpath('nickname', xpath='.//div[@class="left"]/a[@class="u"]/text()')
        user_item_loader.add_xpath('signature', xpath='//div[@class="sign"]/text()')
        yield user_item_loader.load_item()
        # 解析回帖
        reply_item_loader = ItemLoader(item=HupubbsReplyItem(), selector=selector)
        reply_item_loader.add_value('thread_forum_id', value=self.thread_id(response.url))
        reply_item_loader.add_xpath('forum_id', xpath='.//a[@class="floornum"]/@href', re='#([0-9]+)$')
        reply_item_loader.add_xpath('user_forum_id', xpath='.//div[@class="left"]/a[@class="u"]/@href', re='\/([0-9]+)$')
        reply_item_loader.add_xpath('post_time', xpath='.//div/span[@class="stime"]/text()')
        reply_item_loader.add_xpath('i_like_sum', xpath='.//span[contains(@class, "ilike")]/span[@class="stime"]/text()')
        yield reply_item_loader.load_item()
