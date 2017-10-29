# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class AjwItem(scrapy.Item):
    # define the fields for your item here like:

    #地区名字
    region = scrapy.Field()


    #小区名字
    name = scrapy.Field()


    #地方
    address = scrapy.Field()


    #价钱
    price = scrapy.Field()


