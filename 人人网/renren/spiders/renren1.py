# -*- coding: utf-8 -*-
import scrapy


class Renren1Spider(scrapy.Spider):
    name = 'renren1'
    allowed_domains = ['renren.com']
    #start_urls = ['http://www.renren.com/PLogin.do']

    # 当我们重写了start_requests的时候，start_urls列表和parse方法就没有特定的意义了
    def start_requests(self):
        url = 'http://www.renren.com/PLogin.do'

        # 发送post请求登录成功，Scrapy就自动记录了登录状态的Cookie
        # 之后发送任何页面的请求，都会附带这个Cookie
        yield scrapy.FormRequest(
            url = url,
            formdata = {"email" : "mr_mao_hacker@163.com", "password" : "alarmchime"},
            callback = self.parse)

    def parse(self, response):
        yield scrapy.Request("http://www.renren.com/410043129/profile", callback = self.after_login)

    def after_login(self, response):
        with open("my_renren1.html", "w") as f:
            f.write(response.body)


