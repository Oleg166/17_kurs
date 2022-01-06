# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient


class InstaparserPipeline:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongobase = client.instagram

    def process_item(self, item, spider):
        collection = self.mongobase[item['username_main']]
        # в базу данных сохраняются все записи
        """
        # в базу данных сохраняются только уникальные записи (проверка происходит по ссылке)
        username = item['username']
        usertype = item['usertype']
        if collection.count_documents({'username': username, 'usertype': usertype}) > 0:
            pass
        else:
            collection.insert_one(item)"""
        collection.insert_one(item)
        return item
