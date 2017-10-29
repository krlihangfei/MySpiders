# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals


from selenium import webdriver
from .settings import USER_AGENT_LIST
import random

import scrapy
import time
# 导入selenium的报头对象
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities



class SeleniumLeware(object):


    def process_request(self,request,spider):




        # 进入浏览器设置
        options = webdriver.ChromeOptions()
        # 设置中文
        options.add_argument("accept-language='zh-CN,zh;q=0.8'")
        # 更换头部
        options.add_argument(
            'user-agent="Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36"')

        options.add_argument("upgrade-insecure-requests='1'")
        options.add_argument("referer='%s'"%request.url)
        options.add_argument("cookie='__jdv=122270672|baidu|-|organic|not set|1507254244307; ipLoc-djd=1-72-2799-0; user-key=ea37e1ed-49e3-4c91-ad7d-7d7e7dc4d0aa; cn=0; listck=1726303ecdbd7f1e999100a60bb05967; __jda=122270672.1507094260153126264396.1507094260.1508204904.1508207017.12; __jdb=122270672.16.1507094260153126264396|12.1508207017; __jdc=122270672; __jdu=1507094260153126264396; 3AB9D23F7A4B3C9B=U5L5HA33S55IVMWB43ZRRA6Q5VUFYNJ3IIUOKOQIU4X7LQPUGIKRDIISN7WOMGFLCA577CVADZHY7A7C6TIN7M7OTU'")
        options.add_argument("accept-encoding='gzip, deflate, br'")
        options.add_argument("accept='text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8'")
        options.add_argument("scheme='https'")
        url = "https://coll.jd.com"+request.url
        options.add_argument("path='%s'"%url)
        options.add_argument("scheme='https'")
        options.add_argument("authority='list.jd.com'")
        options.add_argument("method='GET'")
        driver = webdriver.Chrome(chrome_options=options)

        url = request.url
        driver.get(url)

        # 执行JS语句
        a=500

        for i in range(17):

            driver.execute_script("var q=document.documentElement.scrollTop=%d"%a)
            time.sleep(0.8)
            a+=500

        #获取页面的源码
        html = driver.page_source
        driver.quit()


        return scrapy.http.HtmlResponse(url=request.url,body=html,encoding="utf-8",request=request)
