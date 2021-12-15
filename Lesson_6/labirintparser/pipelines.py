# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient


class LabirintparserPipeline:

    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongobase = client.book

    def process_item(self, item, spider):
        collection = self.mongobase[spider.name]
        # в базу данных сохраняются только уникальные записи (проверка происходит по ссылке)
        link = item['link']
        if collection.count_documents({'link': link}) > 0:
            pass
        else:
            collection.insert_one(item)
        return item
