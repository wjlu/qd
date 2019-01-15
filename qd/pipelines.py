# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo
import time
from qd.items import UserItem
from scrapy.conf import settings
from qd import emailSender
import logging

# class TimestampPipeline(object):
#     def process_item(self, item, spider):
#         if isinstance(item, UserItem):
#             if item.get('content'):
#                 item['content'] = item['content'].strip().replace('\n','').replace('\r','').replace('\xa0','')
#             if item.get('title'):
#                 item['title'] = item['title'].strip().replace('\n','').replace('\r','').replace('\xa0','')
#             if item.get('timestamp'):
#                 item['date'] = time.strftime("%Y年%m月%d日 %H:%M:%S", time.localtime(item.get('timestamp')))
#         return item


# class MongoPipeline(object):
#     def process_item(self, item, spider):
#         return item


class MongoPipeline(object):
    collection_name = settings.get('CO')

    def __init__(self, mongo_uri, mongo_db):
        self.logger = logging.getLogger(__name__)
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=settings.get('MONGO_URI'),
            mongo_db=settings.get('MONGO_DATABASE')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        # self.logger.debug(item)
        myquery = {"data": item['data']}
        id = {"title": item['title']}
        # 没有找到则插入表，设置字段为1，并用这个字段判断发送邮件
        # db.users.find({"id": '0b3ab35e6a6902'}).count();
        if self.db[self.collection_name].find(myquery).count() == 0:
            # b 对mongodb 插入数据并置位1
            print('插入新字段')
            self.db[self.collection_name].update_one(id,{'$set':{'data': item['data'],'send' :'0'}},upsert=True)
        # els self.db[self.collection_name].find(myquery).count() == 1:
        else:
            # item['purl'] = '1'
            self.db[self.collection_name].update_one(myquery, {'$set':{'send': '1'}})

        return item

