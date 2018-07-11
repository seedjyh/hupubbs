# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class HupubbsItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    forum_name = scrapy.Field()
    total_theme_count = scrapy.Field()
    total_reply_count = scrapy.Field()
    today_post_count = scrapy.Field()
    url = scrapy.Field()
    project = scrapy.Field()
    spider = scrapy.Field()
    server = scrapy.Field()
    date = scrapy.Field()
    pass

class HupubbsSubjectItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    poster_user_url = scrapy.Field()
    poster_nickname = scrapy.Field()
    url = scrapy.Field()
    project = scrapy.Field()
    spider = scrapy.Field()
    server = scrapy.Field()
    date = scrapy.Field()
    pass