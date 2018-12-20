# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ElasticscrapyItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    url = scrapy.Field()
    canonicalId = scrapy.Field()
    title = scrapy.Field()
    sectionTitles = scrapy.Field()
    content = scrapy.Field()
    pageNumber = scrapy.Field()
    lastUpdated = scrapy.Field(serializer=str)
