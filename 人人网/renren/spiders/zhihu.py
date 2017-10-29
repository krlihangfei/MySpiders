# -*- coding: utf-8 -*-
import scrapy
import time

class ZhihuSpider(scrapy.Spider):
    name = 'zhihu'
    allowed_domains = ['zhihu.com']
    start_urls = ['https://www.zhihu.com/#signin']

    def parse(self, response):
        #_xsrf = response.xpath("//input[@name='_xsrf']/@value").extract()[0]
        self._xsrf = response.css("input[name=_xsrf]::attr(value)").extract()[0]
        captcha_url = "https://www.zhihu.com/captcha.gif?r=" + str(int(time.time() * 1000)) + "&type=login"
        # 验证码图片的get请求，同时传递_xsrf
        yield scrapy.Request(captcha_url, meta={"_xsrf" : _xsrf}, callback = self.zhihu_login)


    def parse_captcha(self, response):
        with open("captcha.png", "wb") as f:
            f.write(response.body)
        captcha = raw_input("请输入验证码:")
        return captcha

    def zhihu_login(self, response):
        # 接收_xsrf值
        _xsrf = response.meta["_xsrf"]

        # 构建Form表单数据
        formdata = {
            "_xsrf" : _xsrf,
            "email" : "123636274@qq.com",
            "password" : "ALARMCHIME",
            "captcha" : self.parse_captcha(response)
        }

        # 登录的post请求
        yield scrapy.FormRequest("https://www.zhihu.com/login/email",
                formdata = formdata,
                callback = self.after_login)

    def after_login(self, response):
        # 登录成功后，获取了Cookie，就可以发送其他页面的请求了
        yield scrapy.Request("https://www.zhihu.com/settings/account", callback = self.parse_page)

    def parse_page(self, response):
        with open("my_zhihu.html", "w") as f:
            f.write(response.body)





