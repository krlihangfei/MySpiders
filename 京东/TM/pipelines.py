# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
import os
class TmPipeline(object):

    def process_item(self, item, spider):
        # try:
            print('+++++++++*'*30)
            item = dict(item)
            name1 = item.pop('name1')
            name2 = item.pop('name2')
            name3 = item.pop('name3')


            # 如果目录不存在，则创建目录

            if (not os.path.exists(name1)):
                os.mkdir(name1)

            if (not os.path.exists(name1+'/'+name2)):
                os.mkdir(name1+'/'+name2)

            # 如果目录不存在，则创建目录
            add = name1 + '/' + name2 + '/' + name3 + '.json'



            item_json = json.dumps(item,ensure_ascii=False)

            try:
                print(add)
                with open(add,'a')as f:
                    f.write(item_json+',\n')
                    print('写入成功....')
            except:

                with open('失败商品.text','a')as f:
                    f.write(name3+'\n')
                print('写入失败．．．')

            return item
