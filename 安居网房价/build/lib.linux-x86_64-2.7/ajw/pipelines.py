# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import os
# import pymongo
import json
from scrapy.pipelines.images import ImagesPipeline
class AjwPipeline(object):

    def process_item(self, item, spider):

        # url = 'pass/'+item['region']+'.json'

        # 如果目录不存在，则创建目录
        if (not os.path.exists(item['region']+'.json')):
            os.mknod(item['region']+'.json')
        item  = dict(item)

        item_json = json.dumps(item,ensure_ascii=False)+',\n'

        add =item['region']+'.json'

        with open(add,'a')as f:

            f.write(item_json)
            print('写入完成-------------')

        return item


# #写入ｍｏｎｇｏ数据库
# class AjwMongoDBPipeline(object):
#
#     def __init__(self):
#         #创建mongoDB数据库
#
#         self.client = pymongo.MongoClient(host="127.0.0.1",port=27017)
#
#         #指定ＭｏｎｇｏＤＢ的数据库
#
#         self.db_name = self.client["price"]
#
#         #指定数据库表名
#         self.sheet_name = self.db_name['jiaqiang']
#
#
#     def process_item(self,item,spider):
#
#         #向表插入数据，参数是一个字典
#         self.sheet_name.insert(dict(item))
#         return item









