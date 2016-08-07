# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from pymongo import MongoClient
from subscribe import *

class BlogPipeline(object):

    db_name = 'blog'
    collection_name = 'post'

    def add_to_collection(self, col, item):
        title = item['title']
        post = col.find_one({'title': title})	
        print(post)
        if not post:
            col.insert(item)

    def process_item(self, item, spider):
        desc = dict(item)
        self.add_to_collection(self.col, desc)
        return item

    def open_spider(self, spider):
        self.client = MongoClient('mongodb://localhost:27017/')
        self.db = self.client[self.db_name]
        self.col = self.db[self.collection_name]

    def close_spider(self, spider):
        Subscribe(self.col).start()
        self.client.close()

