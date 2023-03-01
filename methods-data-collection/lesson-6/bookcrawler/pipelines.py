# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient


class BookcrawlerPipeline:
    def __init__(self):
        """
        Конструктор.
        """
        client = MongoClient('localhost', 27017)
        self.storage = client.parser_db['books']

    def process_item(self, item, spider):
        """
        Сохранение и обработка данных
        :param item:
        :param spider:
        :return:
        """
        item['price'] = float(item['price'])
        if item['sale_price']:
            item['sale_price'] = float(item['sale_price'])
        if item['rate']:
            item['rate'] = float(item['rate'])

        self.storage.update_one(item, {'$setOnInsert': item}, upsert=True)
        return item