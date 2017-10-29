# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TmItem(scrapy.Item):
    # define the fields for your item here like:
    jiaqiang = scrapy.Field()

    name = scrapy.Field()

    url = scrapy.Field()

    ren = scrapy.Field()

    name1 = scrapy.Field()
    name2 = scrapy.Field()
    name3 = scrapy.Field()


