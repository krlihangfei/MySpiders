# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from ..items import AjwItem

class FangjiaSpider(CrawlSpider):
    name = 'fangjia'
    # allowed_domains = ['leju.com']
    start_urls = ['http://house.leju.com/tz/search/']

    link_list = []
    rules = (
        #提取需要爬起的ｕｒｌ
        Rule(LinkExtractor(allow=(r'http://house.leju.com/[a-z][a-z]/search/'),deny=(r'(html|#)')),callback='parse_item',follow=False),
        # #获取　页面的其他页面的ｕｒｌ
        # Rule(LinkExtractor(allow=(r'http://house\.leju\.com/bj/search/page\d+?\.html#wt_source=pc_search_down_fy'),
        #                    deny=(r"#wt_source=pc_search_fy")),callback='parse_item', follow=True),

    )

    def parse_item(self, response):


        self.link_list.append(response.url)





        with open('hh1.text','a')as f:
            f.write(response.url+'\n')

        item = AjwItem()


        #地区名字
        item['region'] = response.xpath("//div[@class='city']/span/text()").extract()[0]

        #全部房子
        xp_name =response.xpath("//div[@id='ZT_searchBox']/div[@class='b_card']")

        for room in xp_name:
            #小区名字
            item['name'] = room.xpath(".//div[@class='b_titBox']/h2/a/text()").extract()[0]


            #小区在怎么地方
            s=room.xpath(".//div[@class='b_titBox']/h3/text()").extract()[0]
            dictStr = s.rfind(']')
            item['address'] = s[2:dictStr]


            #价钱
            try:
                item['price'] = room.xpath(".//div[@class='b_infoBox']/h2/strong/text()").extract()[0]


            except:
                item['price']='尚未公布'


            yield item

        #
        if response.xpath("//div[@class='b_pages clearfix']/a[@class='next']"):
            url = response.xpath("//div[@class='b_pages clearfix']/a[@class='next']/@href").extract()[0]

            yield scrapy.Request(url,callback=self.parse_item)






