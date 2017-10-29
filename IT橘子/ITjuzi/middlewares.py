# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html


import scrapy

class ProxyMiddleware(object):
    def process_request(self, request, spider):
        proxy = "mr_mao_hacker:sffqry9r@116.62.128.50:16816"
        request.meta["proxy"] = "http://" + proxy

