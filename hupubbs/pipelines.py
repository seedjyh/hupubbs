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
        self.db = pymysql.connect("127.0.0.1", "root", "123456", "hupubbs")
        self.cursor = self.db.cursor()

    def close_spider(self, spider):
        self.db.close()

    def process_item(self, item, spider):
        switcher = {
            HupubbsUserItem: self.process_user_item,
            HupubbsSubjectItem: self.process_subject_item,
            HupubbsReplyItem: self.process_reply_item,
            HupubbsPlateItem: self.process_plate_item,
        }
        switcher.get(type(item), lambda: "")()
        return item

    def process_user_item(self, item, spider):
        pass

    def process_plate_item(self, item, spider):
        pass

    def process_subject_item(self, item, spider):
        pass

    def process_reply_item(self, item, spider):
        pass
