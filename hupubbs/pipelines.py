# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql
from hupubbs.items import HupubbsUserItem, HupubbsPlateItem, HupubbsSubjectItem, HupubbsReplyItem

class HupubbsPipeline(object):
    def open_spider(self, spider):
        print('++++++++++++++++++ OPEN SPIDER ++++++++++++++++++')
    def close_spider(self, spider):
        print('.................. CLOSE SPIDER ..................')
    def process_item(self, item, spider):
        print('----------------------------------------------------------------')
        print(item)
        return item


class MySQLPipeline(object):
    def open_spider(self, spider):
        self.db = pymysql.connect(
            host='127.0.0.1',
            port=9306,
            user='root',
            passwd='123456',
            db='hupubbs',
            charset='utf8'
        )
        self.cursor = self.db.cursor()

    def close_spider(self, spider):
        self.db.commit()
        self.db.close()

    def process_item(self, item, spider):
        switcher = {
            HupubbsUserItem: self.process_user_item,
            HupubbsSubjectItem: self.process_subject_item,
            HupubbsReplyItem: self.process_reply_item,
            HupubbsPlateItem: self.process_plate_item,
        }
        switcher.get(type(item), lambda: "")(item, spider)
        return item

    def process_user_item(self, item, spider):
        values = (
            item.get('url_id'),
            item.get('nickname'),
            [str.strip(x) for x in item.get('signature', ['', ])],  # 签名默认值：空串
        )
        self.cursor.execute("INSERT IGNORE INTO user(url_id, nickname, signature) VALUES(%s,%s,%s)", values)

    def process_plate_item(self, item, spider):
        values = (
            item.get('name'),
            item.get('url'),
        )
        self.cursor.execute("INSERT IGNORE INTO plate(name, url) VALUES(%s,%s)", values)

    def process_subject_item(self, item, spider):
        values = (
            item.get('url_id'),
            item.get('plate_url'),
            item.get('user_url_id'),
            item.get('post_time'),
            item.get('title'),
        )
        self.cursor.execute(
            "INSERT IGNORE INTO thread(url_id, plate_id, user_id, post_time, title) VALUES(%s, (select id from plate where url=%s), (select id from user where url_id=%s), %s, %s)",
            values)

    def process_reply_item(self, item, spider):
        values = (
            item.get('thread_url_id'),
            item.get('url_id'),
            item.get('user_url_id'),
            item.get('post_time'),
            item.get('i_like_sum'),
        )
        self.cursor.execute(
            "INSERT IGNORE INTO reply(thread_id, url_id, user_id, post_time, i_like_sum) VALUES((select id from thread where url_id=%s), %s, (select id from user where url_id=%s), %s, %s)",
            values)
