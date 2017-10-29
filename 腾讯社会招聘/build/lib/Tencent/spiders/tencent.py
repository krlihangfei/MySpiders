# -*- coding: utf-8 -*-
import scrapy
from Tencent.items import TencentItem

#scrapy.CrawlSpider

class TencentSpider(scrapy.Spider):
    name = 'tencent'
    allowed_domains = ['hr.tencent.com']

    base_url = "http://hr.tencent.com/position.php?&start="
    offset = 0
    start_urls = [base_url + str(offset)]

    # start_urls 里的url地址不做去重（不记录请求指纹）
    #start_urls = [base_url + str(num) for num in range(0, 2200 + 1, 10)]

    def parse(self, response):
        node_list = response.xpath("//tr[@class='even'] | //tr[@class='odd']")

        for node in node_list:
            item = TencentItem()

            item['position_name'] = node.xpath("./td[1]/a/text()").extract()[0]
            item['position_link'] = "http://hr.tencent.com/" + node.xpath("./td[1]/a/@href").extract()[0]

            try:
                item['position_type'] = node.xpath("./td[2]/text()").extract()[0]
            except:
                item['position_type'] = "None"

            #position_type_list = node.xpath("./td[2]/text()").extract()
            #item['position_type'] = position_type_list[0] if position_type_list else "None"

            item['people_number'] = node.xpath("./td[3]/text()").extract()[0]
            item['work_location'] = node.xpath("./td[4]/text()").extract()[0]
            item['publish_times'] = node.xpath("./td[5]/text()").extract()[0]

            yield item


        #if self.offset < 2200:
        #    self.offset += 10
        #    # scrapy.Request() 构建一个请求，第一个参数是url，callback 指定回调函数，表示该请求返回的response由哪个方法来解析
        #    yield scrapy.Request(self.base_url + str(self.offset), callback = self.parse)

        # 如果是不同标签里判断属性, 用 | 表示或
        #"//tr[@class='even'] | //tr[@class='odd']"

        # 如果同一个标签内判断属性，用 and  表示与
        # 如果到了最后一页，则列表为空，判断条件为False，不再发送请求；not 取反表示继续发送请求
        if not response.xpath("//a[@class='noactive' and @id='next']"):
            next_link = "http://hr.tencent.com/" + response.xpath("//a[@id='next']/@href").extract()[0]
            yield scrapy.Request(next_link, callback = self.parse)



