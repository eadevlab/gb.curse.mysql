from itemadapter import ItemAdapter
from pymongo import MongoClient
import pprint


class CrawlerPipeline:
    """Пайплайн."""
    def __init__(self):
        """Кнструктор."""
        self.client = MongoClient('localhost', 27017)

    def process_item(self, item, spider):
        storage = self.client[spider.db_name][spider.collection]
        storage.update_one(item, {'$setOnInsert': item}, upsert=True)
        print('='*10)
        pprint.pprint(item)
        print('='*10)
        return item
