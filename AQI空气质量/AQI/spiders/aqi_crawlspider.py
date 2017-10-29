# coding:utf-8

import scrapy

#from scrapy.spiders import CrawlSpider, Rule
from scrapy.spiders import Rule
# 1. 导入使用的爬虫类RedisCrawlSpider
from scrapy_redis.spiders import RedisCrawlSpider

from scrapy.linkextractors import LinkExtractor
from AQI.items import AqiItem

# 2. 修改继承的父类
#class AqiSpider(CrawlSpider):
class AqiCrawlSpider(RedisCrawlSpider):

    name = "aqi_crawlspider"
    allowed_domains = ["aqistudy.cn"]
    #start_urls = ["https://www.aqistudy.cn/historydata/"]
    # 3. 指定redis_key
    redis_key = "aqi_crawlspider"

    rules = (
        # 提取每个城市的的链接，返回该城市所有月份的响应
        # 如果没有指定回调函数，则表示这个链接提取是跳板，不需要回调函数，follow默认为True
        Rule(LinkExtractor(allow=r"monthdata\.php\?city=")),
        # 提取每个月的链接，返回每一天的数据响应
        # 指定回调函数，follow默认为False
        Rule(LinkExtractor(allow=r"daydata\.php\?city="), callback = "parse_item")
    )


    def parse_item(self, response):
        node_list = response.xpath("//tr")
        node_list.pop(0)

        # extract_first() 直接获取列表里的第一个元素并返回（不会返回列表）
        # extract() 返回列表
        city_name = response.xpath("//h3[@id='title']/text()").extract_first()

        for node in node_list:
            item = AqiItem()
            item['city'] = city_name[8:-11]
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
