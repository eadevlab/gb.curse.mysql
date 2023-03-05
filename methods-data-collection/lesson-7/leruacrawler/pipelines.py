import os.path
import sys

import scrapy
from itemadapter import ItemAdapter
from pymongo import MongoClient
from scrapy.pipelines.images import ImagesPipeline

class ProductPipeline:
    """Пайплайн товара"""
    def __init__(self):
        """Кнструктор"""
        client = MongoClient('localhost', 27017)
        self.storage = client.parser_db['catalog']

    def process_item(self, item, spider):
        item['params'] = dict(
            zip(item['tmp_param_names'], item['tmp_param_values'][:len(item['tmp_param_names'])])
        )

        # Удалим временные значения
        del item['tmp_param_names']
        del item['tmp_param_values']

        self.storage.update_one(item, {'$setOnInsert': item}, upsert=True)
        return item



class ProductImagesPipeline(ImagesPipeline):
    """Пайплайн изображений"""
    def get_media_requests(self, item, info):
        print(item['images'])
        if item['images']:
            for _ in item['images']:
                yield scrapy.Request(_)

    def file_path(self, request, response=None, info=None, *, item=None):
        return f"{item.get('_id')}/{os.path.basename(request.url)}"