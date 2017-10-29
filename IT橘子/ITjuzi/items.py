# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ItjuziItem(scrapy.Item):

    # cpy1: 基本信息
    name = scrapy.Field()
    slogan = scrapy.Field()
    scope_big = scrapy.Field()
    scope_little = scrapy.Field()
    province = scrapy.Field()
    city = scrapy.Field()
    home_link = scrapy.Field()
    tag = scrapy.Field()

    # cpy2：公司信息
    company_info = scrapy.Field()
    company_fullname = scrapy.Field()
    company_time = scrapy.Field()
    company_size = scrapy.Field()
    company_status = scrapy.Field()

    # cpy3：融资信息
    financing = scrapy.Field()
    financing_time = scrapy.Field()
    financing_stage = scrapy.Field()
    financing_money = scrapy.Field()
    financing_company = scrapy.Field()


    # cp4：团队信息
    team = scrapy.Field()
    team_name = scrapy.Field()
    team_title = scrapy.Field()
    team_info = scrapy.Field()


    # cpy5: 产品信息
    product = scrapy.Field()
    product_name = scrapy.Field()
    product_type = scrapy.Field()
    product_info = scrapy.Field()


    utc_time = scrapy.Field()
    source = scrapy.Field()


    # shift + 鼠标右击拖动
