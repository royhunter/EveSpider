# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class JobspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name = scrapy.Field()
    createtime = scrapy.Field()
    updatetime = scrapy.Field()
    desc = scrapy.Field()
    requirement = scrapy.Field()
    departmentName = scrapy.Field()
    category = scrapy.Field()
    workExperience = scrapy.Field()
    jobid = scrapy.Field()
    pass
