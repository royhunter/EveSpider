# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from pymongo import MongoClient
from subscribe import *

class JobspiderPipeline(object):
    db_name = 'ali'
    collection_name = 'job'

    def add_to_collection(self, col, item):
        name = item['name']
        post = col.find_one({'name': name})   
        if not post:
            col.insert(item)

    def process_item(self, item, spider):
        job = dict(item)
        self.add_to_collection(self.col, job)
        return item

    def open_spider(self, spider):
        self.client = MongoClient('mongodb://localhost:27017/')
        self.db = self.client[self.db_name]
        self.col = self.db[self.collection_name]

    def close_spider(self, spider):
        Subscribe(self.col).start()
        self.client.close()