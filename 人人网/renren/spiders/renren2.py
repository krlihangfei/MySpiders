# -*- coding: utf-8 -*-
import scrapy


class Renren2Spider(scrapy.Spider):
    name = 'renren2'
    allowed_domains = ['renren.com']
    #start_urls = ['http://renren.com/']

    cookies = {
        "anonymid" : "j7wsz80ibwp8x3",
        "_r01_" : "1",
        "depovince" : "GW",
        "JSESSIONID" : "abcrEdlaMwrf3g1XOif8v",
        "ch_id" : "10016",
        "wp_fold" : "0",
        "jebecookies" : "8a2da242-d340-4caf-9e1e-64b63ec0ce51|||||",
        "ick_login" : "d313b9c6-011b-4bc3-bc5c-711c9f95ca36",
        "_de" : "BF09EE3A28DED52E6B65F6A4705D973F1383380866D39FF5",
        "p" : "7377d857a8610764629cbb7088b840ec9",
        "ap" : "327550029",
        "first_login_flag" : "1",
        "ln_uact" : "mr_mao_hacker@163.com",
        "ln_hurl" : "http://hdn.xnimg.cn/photos/hdn321/20171010/1010/main_sYAL_10ae00000f81195a.jpg",
        "t" : "410c9a327330833f14e0f216f165b1e19",
        "societyguester" : "410c9a327330833f14e0f216f165b1e19",
        "id" : "327550029",
        "xnsid" : "faaa3f2d",
        "loginfrom" : "syshome",
        "springskin" : "set",
        "WebOnLineNotice_327550029" : "1",
    }

    def start_requests(self):
        url = "http://www.renren.com/410043129/profile"
        yield scrapy.Request(url = url, cookies = self.cookies, callback = self.parse)
        yield scrapy.Request(url = "http://www.renren.com/436310609/profile", cookies = self.cookies, callback = self.parse)

    def parse(self, response):
        with open(response.url[-20:].replace("/","_") + ".html", "w") as f:
            f.write(response.body)
