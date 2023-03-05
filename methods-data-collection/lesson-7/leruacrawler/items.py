# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import TakeFirst, MapCompose


def price_format(value):
    """
    Преобразование типа цены
    :param value:
    :return:
    """
    try:
        value = float(value)
    except ValueError:
        value = 0
    return value

def id_format(value):
    """
    Преробрахование аритикула
    :param value:
    :return:
    """
    value = value.replace('Артикул:','')
    value = value.strip()
    return value


def clear_value(value:str) -> str:
    """
    Очистка значения от лишнего
    :param value:
    :return:
    """
    value = value.strip()
    return value


class ProductItem(scrapy.Item):
    """
    Модель товара.
    """
    _id = scrapy.Field(output_processor=TakeFirst(),input_processor=MapCompose(id_format))  # Артикул товара
    name = scrapy.Field(output_processor=TakeFirst(),input_processor=MapCompose(clear_value))  # Название товара
    images = scrapy.Field()  # Изображения
    price = scrapy.Field(output_processor=TakeFirst(), input_processor=MapCompose(price_format))  # Цена
    url = scrapy.Field(output_processor=TakeFirst())  # Ссылка
    params = scrapy.Field()  # Характеристики товара
    tmp_param_names = scrapy.Field(input_processor=MapCompose(clear_value)) # Временное хранилище для хранения названий характеристик
    tmp_param_values = scrapy.Field(input_processor=MapCompose(clear_value)) # Временное хранилище для хранения значений характеристик
