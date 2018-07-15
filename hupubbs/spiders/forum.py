# -*- coding: utf-8 -*-
import scrapy
import re
from scrapy.http import Request
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from hupubbs.items import HupubbsUserItem, HupubbsSubjectItem, HupubbsReplyItem, HupubbsPlateItem


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
        return Request(response.url, callback=self.parse_plate_page)

    # 爬取某版块的某一页
    def parse_plate_page(self, response):
        # 解析版块item
        plate_item_loader = ItemLoader(item=HupubbsPlateItem(), response=response)
        plate_item_loader.add_xpath('name', xpath='//span[@id="forumname"]/text()')
        plate_item_loader.add_value('url', value=response.url)
        yield plate_item_loader.load_item()
        # 横向：下一页
        yield Request(self.next_forum_page_url(response.url), self.parse_plate_page)
        # 纵向：子版块
        le = LinkExtractor(restrict_xpaths='//div[@id="childBoards"]')
        for link in le.extract_links(response):
            yield Request(link.url, self.parse_plate_page)
        # 纵向：当前页所有主题
        le = LinkExtractor(restrict_xpaths='//a[@class="truetit"]')
        links = le.extract_links(response)
        for link in links:
            yield Request(link.url, callback=self.parse_thread_page)

    # 爬取单个主题
    def parse_thread_page(self, response):
        # 横向：下一页
        yield Request(self.next_thread_page_url(response.url), self.parse_thread_page)
        # 当页：主楼（0个或1个）
        selectors = response.xpath('//form/div[@id="tpc"]')
        if len(selectors) >= 1:
            for item in self.parse_subject(selectors[0], response):
                yield item
        # 当页：高亮
        # selectors = response.xpath('//form/div[contains(@class, "w_reply")]//div[@class="floor"]')
        # 当页：回复
        selectors = response.xpath('//form/div[@id!="tpc"][@class = "floor"]')
        for selector in selectors:
            for item in self.parse_reply(selector, response):
                yield item

    # 解析顶楼
    def parse_subject(self, selector, response):
        # 解析所属版块
        le = LinkExtractor(restrict_xpaths='//div[@itemprop="breadcrumb"]')
        plate_links = le.extract_links(response)
        plate_link = plate_links[-1]
        # 解析发帖人
        user_item_loader = ItemLoader(item=HupubbsUserItem(), selector=selector)
        user_item_loader.add_xpath('url_id', xpath='.//a[@class="u"]/@href', re='\/([0-9]+)$')
        user_item_loader.add_xpath('nickname', xpath='.//a[@class="u"]/text()')
        user_item_loader.add_xpath('signature', xpath='//div[@class="sign"]')
        user_item = user_item_loader.load_item()
        yield user_item
        # 解析主题帖
        subject_item_loader = ItemLoader(item=HupubbsSubjectItem(), selector=selector)
        subject_item_loader.add_value('url_id', value=self.thread_id(response.url))
        subject_item_loader.add_value('plate_url', value=plate_link)
        subject_item_loader.add_value('user_url_id', user_item['url_id'])
        subject_item_loader.add_xpath('post_time', xpath='.//span[@class="stime"]/text()')
        subject_item_loader.add_xpath('title', xpath='.//div[@class="subhead"]/span/text()')
        yield subject_item_loader.load_item()

    # 解析回帖
    def parse_reply(self, selector, response):
        # 解析回帖人
        user_item_loader = ItemLoader(item=HupubbsUserItem(), selector=selector)
        user_item_loader.add_xpath('url_id', xpath='.//div[@class="left"]/a[@class="u"]/@href', re='\/([0-9]+)$')
        user_item_loader.add_xpath('nickname', xpath='.//div[@class="left"]/a[@class="u"]/text()')
        user_item_loader.add_xpath('signature', xpath='//div[@class="sign"]/text()')
        user_item = user_item_loader.load_item()
        yield user_item
        # 解析回帖
        reply_item_loader = ItemLoader(item=HupubbsReplyItem(), selector=selector)
        reply_item_loader.add_value('thread_url_id', value=self.thread_id(response.url))
        reply_item_loader.add_xpath('url_id', xpath='.//a[@class="floornum"]/@href', re='#([0-9]+)$')
        reply_item_loader.add_value('user_url_id', value=user_item['url_id'])
        reply_item_loader.add_xpath('post_time', xpath='.//div/span[@class="stime"]/text()')
        reply_item_loader.add_xpath('i_like_sum', xpath='.//span[contains(@class, "ilike")]/span[@class="stime"]/text()')
        yield reply_item_loader.load_item()
