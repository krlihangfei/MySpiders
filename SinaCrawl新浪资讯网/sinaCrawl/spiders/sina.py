# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import os
from sinaCrawl.items import SinaItem


class SinaSpider(CrawlSpider):
    name = 'sina'
    allowed_domains = ['sina.com.cn']
    start_urls = ['http://news.sina.com.cn/guide/']

    rules = (
        Rule(LinkExtractor(allow=r'sina.com.cn', restrict_xpaths=r"//div[@id='tab01']/div/ul/li/a"),
             callback='second_parse',
             follow=False),
    )

    def parse_start_url(self, response):
        s = response.xpath("//div[@id='tab01']//a/text()").extract_first()
        print(s)
        print("-----------------ABCD")

    def second_parse(self, response):

        # meta_1 = response.meta["meta_1"]

        parentFilename = "./Data/" + response.url.split('/')[2].split('.')[0]

        subTitle = response.url.split('/')[3]

        if not os.path.exists(parentFilename):
            os.makedirs(parentFilename)

        subFilename = parentFilename + '/' + subTitle

        if not os.path.exists(subFilename):
            os.makedirs(subFilename)

        sonUrls = response.xpath('//a/@href').extract()

        items = []

        for i in range(0, len(sonUrls)):
            if_belong = sonUrls[i].endswith('.shtml') and sonUrls[i].startswith(response.url)

            if if_belong:
                item = SinaItem()
                item['subFilename'] = subFilename
                item['sonUrls'] = sonUrls[i]
                items.append(item)

        for item in items:
            yield scrapy.Request(url=item['sonUrls'], meta = {'meta_2': item}, callback=self.detail_parse)

    def detail_parse(self, response):
        item = response.meta['meta_2']

        # head = response.xpath('//h1/text()').extract()[0]
        content = "".join(response.xpath('//p/text()').extract())

        # item['head'] = head
        item['content'] = content.strip()

        yield item