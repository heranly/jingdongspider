# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class JingdongItem(scrapy.Item):
    # define the fields for your item here like:
    filename = scrapy.Field()
    intruduce = scrapy.Field()
    img_urls = scrapy.Field()
    good_id = scrapy.Field()
    img_name = scrapy.Field()


class JingdongItem2(scrapy.Item):
    # define the fields for your item here like:
    filename = scrapy.Field()
    page = scrapy.Field()
    contents_Urls = scrapy.Field()
    contents = scrapy.Field()
    productColors = scrapy.Field()

