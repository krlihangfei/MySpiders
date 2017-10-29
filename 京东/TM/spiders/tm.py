# -*- coding: utf-8 -*-
import scrapy
from ..items import TmItem
import json
import re
import os
import time
class TmSpider(scrapy.Spider):
    name = 'tm'
    # allowed_domains = ['baidu.xom']
    start_urls = ['https://dc.3.cn/category/get?callback=getCategoryCallback']

    #全部数据ｕｒｌ
    list_name = []

    def parse(self, response):

        html = response.text
        #清除不需要的数据
        sum=html.find('(')
        html = html[sum+1:-1]
        json_html = json.loads(html[:-20])


        for item in json_html['data']:

            for i in item['s']:

                list_url_name = []

                name = i['n']

                sum = name.find('|')
                url = name[sum + 1:]
                sum = url.find('|')
                url1 = url[:sum]


                item_list = i['s']

                for i in item_list:
                    list = []
                    list.append(url1)

                    item_data = i['s']
                    name_list = i['n']
                    sum = name_list.find("|")
                    url2 = name_list[sum + 1:-3]
                    list.append(url2)
                    list_url_name.append(list)


                    for j in item_data:
                        dict = {}

                        url = j['n']
                        sum = url.find("|")
                        name = url[sum + 1:-3]

                        pattern = re.compile(r'^\d')
                        data = pattern.match(url)

                        if data != None:
                            sum = url.find('|')

                            url = url[:sum]
                            dict[name] = '//list.jd.com/list.html?cat=' + url

                            list_url_name.append(dict)


                        else:
                            sum = url.find('|')

                            url = url[:sum]
                            list_url_name.append(url)


                self.list_name.append(list_url_name)



        yield scrapy.Request("https://www.baidu.com/",meta={'name':self.list_name}, callback=self.request_name)


    def request_name(self,response):

        su = {}
        item = response.meta["name"]


        for url_list in item:

            for url in url_list:

                if type(url) == list:

                    # 如果目录不存在，则创建目录
                    if (not os.path.exists('../data/' + url[0])):
                        os.mkdir('../data/' + url[0])

                    ad = url[1].replace('/', '')

                    if (not os.path.exists('../data/' + url[0] + '/' + ad)):
                        su['val'] = url[0] + '/' + ad
                        os.mkdir('../data/' + url[0] + '/' + ad)

                else:

                    if type(url) != str:

                        name = list(url.keys())[0]
                        names = name.replace('/', '')

                        with open('../data/' + su['val'] + '/' + names + '.json', 'w')as f:
                            pass

                        url = "https:"+url[name]
                        time.sleep(2)
                        yield scrapy.Request(url,callback=self.parse_requset)


    def parse_requset(self,response):


        #全部商品
        itemq = response.xpath("//ul[@class='gl-warp clearfix']/li")
        #类型
        name1 = response.xpath("//div[@class='crumbs-nav-item one-level']/a/text()").extract()[0]
        mingzhi = response.xpath("//div[@class='trigger']/span/text()").extract()
        name2 = mingzhi[0]
        name3 = mingzhi[1]



        for item1 in itemq:

            item =TmItem()

            item['name1']= name1
            item["name2"] = name2
            item["name3"] = name3


            #价钱
            print(item1.xpath(".//strong/i/text()").extract()[0])
            try:
                item['jiaqiang'] = item1.xpath(".//strong/i/text()").extract()[0]
            except:
                item['jiaqiang'] = '空'

            #名字
            item['name']= item1.xpath(".//div[@class='p-name']/a/em/text()").extract()[0].strip()
            print(item1.xpath(".//div[@class='p-name']/a/em/text()").extract()[0].strip())

            # #图片地址
            # try:
            #     item['url']= item.xpath(".//div[@class='p-img']/a/img/@src").extract()[0]
            #
            #     print(item.xpath(".//div[@class='p-img']/a/img/@src").extract()[0])
            # except:
            #     print('空')
            #     item['url'] = '空'
             #评论人数
            print(item1.xpath(".//strong/a/text()").extract()[0])
            item['ren']=item1.xpath(".//strong/a/text()").extract()[0]

            yield item


        if response.xpath("//span[@class='p-num']//a[@class='pn-next']/@href"):

            url= response.xpath("//span[@class='p-num']//a[@class='pn-next']/@href").extract()[0]
            url=url.replace("%5F",'_')
            yield scrapy.Request('https://list.jd.com' +url,callback=self.parse_requset)





