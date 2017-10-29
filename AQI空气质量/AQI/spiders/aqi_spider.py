# -*- coding:utf-8 -*-

import scrapy
# 1. 导入需要的爬虫类
from scrapy_redis.spiders import RedisSpider
from AQI.items import AqiItem

# 2. 修改爬虫类的父类
#class AqiSpider(scrapy.Spider):
class AqiSpider(RedisSpider):
    name = "aqi_spider"
    allowed_domains = ["aqistudy.cn"]

    base_url = "https://www.aqistudy.cn/historydata/"
    redis_key = "aqispider:start_urls"

    #start_urls = [base_url]
    def parse(self, response):
        city_link_list = response.xpath("//div[@class='all']//li/a/@href").extract()
        city_name_list = response.xpath("//div[@class='all']//li/a/text()").extract()

        #index, city_link = enumerate(city_link_list)
        for city_link, city_name in zip(city_link_list, city_name_list)[100:101]:
            yield scrapy.Request(self.base_url + city_link, meta = {"city_name" : city_name}, callback = self.parse_month)

    def parse_month(self, response):
        month_link_list = response.xpath("//td[@align='center']//a/@href").extract()
        for month_link in month_link_list[3:4]:
            yield scrapy.Request(self.base_url + month_link, meta = response.meta, callback = self.parse_day)

    def parse_day(self, response):
        node_list = response.xpath("//tr")
        node_list.pop(0)

        # extract_first() 直接获取列表里的第一个元素并返回（不会返回列表）
        # extract() 返回列表

        for node in node_list:
            item = AqiItem()
            item['city'] = response.meta["city_name"]
            item['date'] = node.xpath("./td[1]/text()").extract()[0]
            item['aqi'] = node.xpath("./td[2]/text()").extract()[0]
            item['level'] = node.xpath("./td[3]/span/text()").extract()[0]
            item['pm2_5'] = node.xpath("./td[4]/text()").extract()[0]
            item['pm10'] = node.xpath("./td[5]/text()").extract()[0]
            item['so2'] = node.xpath("./td[6]/text()").extract()[0]
            item['co'] = node.xpath("./td[7]/text()").extract()[0]
            item['no2'] = node.xpath("./td[8]/text()").extract()[0]
            item['o3'] = node.xpath("./td[9]/text()").extract()[0]

            yield item
