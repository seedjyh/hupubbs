# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql

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
    def close_spider(self, spider):
        self.db.close()
    def process_item(self, item, spider):
        cursor = self.db.cursor()
        cursor.execute('select id, nickname, prosign from user')
        for x in cursor.fetchall():
            print(x)
