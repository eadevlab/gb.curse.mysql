"""
Парсер взят из Урока №3
Немного измененно сохранение результатов
"""
import sys

from bs4 import BeautifulSoup
import requests as req
import re
import json
import csv
import pandas as pd
from pymongo import MongoClient

DB_NAME = 'parser_db'
TABLE_NAME = 'products'

class ParserStorage:
    """
    Класс для хранилища результатов парсера
    """
    def __init__(self, db_name, storage_name, host='localhost', port=27017):
        client = MongoClient(host, port)
        db = client[db_name]
        self.storage = db[storage_name]
    def exists(self, search:dict) -> int:
        """
        Проверка существования документа
        :param search:
        :return:
        """
        return self.storage.count_documents(search)>0

    def find(self, search:dict, order=None) -> list:
        """
        Поиск документов
        :param search: Параметры фильтрации
        :param order: Сортировка
        :return:
        """
        query = self.storage.find(search)
        if order:
            query.sort(order)
        return list(query)

    def create(self, doc:dict) -> str:
        """
        Добавление нового документа
        :param doc:
        :return: Идентификатор добавленного документа
        """
        res = self.storage.insert_one(doc)
        return res.inserted_id

    def update(self, data:dict, search:dict) -> int:
        """
        Обновление записи
        :param data: Обновляемые данные
        :param search: Фильтр
        :return: Количество измененных записей
        """
        if self.exists(search):
            ret = self.storage.update_one(data, search)
            return ret.modified_count
        return 0


class BsParser:
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; rv:76.0) Gecko/20100101 Firefox/76.0",
        "Pragma":"",
        "Cache-Control":"max-age=0"
    }

    def _soup(self, url: str) -> BeautifulSoup:
        """
        Получение объекта BeautifulSoup
        :param url: str Ссылка
        :return:
        """
        resp = req.get(url)
        return BeautifulSoup(resp.text, 'lxml')


class SiteParser(BsParser):
    """
    Класс парсера с помощью Beautiful Soap
    """
    req_keys = ['host','tree','start_url']
    def __init__(self, settings:dict, leaf_parser_class):
        """
        Конструктор.
        :param settings:
        :param leaf_parser_class:
        """
        assert self.__validate(settings) == True
        self.tree = settings['tree']
        self.host = settings['host']
        self.start_url = settings['start_url']
        self.leaf_parser_class = leaf_parser_class

        self.storage = ParserStorage(DB_NAME, TABLE_NAME)

    def __validate(self, settings:dict) -> bool:
        """
        Проверка необходимых ключей
        :param settings:
        :return:
        """
        valid = True
        for req_key in self.req_keys:
            valid &= req_key in settings
        return valid

    def parse(self) -> None:
        """
        Запуск парсера
        :return:
        """
        self._parse_recursive(self.start_url, 0)

    def _parse_recursive(self, url:str, current_level:int):
        """
        Рекурсивный парсинг сайта
        :param url: Ссылка
        :param current_level: Текущий уровень в древе парсинга
        :return:
        """
        tree_item = self.tree[current_level]
        if tree_item['type'] == 'branch':
            for _ in self.__branch_parse(url, tree_item):
                self._parse_recursive(_, current_level+1)
        else:
            for _ in self.__leaf_parse(url, tree_item):
                self.__leaf_save(self.leaf_parser_class(_))

    def __branch_parse(self, url: str, settings: dict):
        """
        Парсинг ветви
        :param url: Ссылка
        :param settings: Настройки
        :return: list[str]
        """
        soup = self._soup(url)
        for node in soup.select(settings['selector']):
            yield self.__prepare_url(node['href'])

    def __leaf_parse(self, url, settings) -> list:
        """
        Парсинг листа древа
        :param url: Ссылка
        :param settings: Настройки
        :return: list
        """
        soup = self._soup(url)
        if settings['data'] == 'html':
            for node in soup.select(settings['selector']):
                yield self.__prepare_url(node['href'])
        elif settings['data'] == 'json':
            json_string = re.search(settings['selector'],
                                    str(soup.findAll('script')))
            if json_string:
                for leaf in json.loads(json_string.group(1)):
                    yield self.__prepare_url(leaf[settings['url_key']])
        else:
            return []

    def __leaf_save(self, provider):
        """
        Сохранение листа в MongoDB
        :param provider:
        :return:
        """
        if not self.storage.exists(provider.to_search()):
            self.storage.create(provider.asdict())

    def __prepare_url(self, url:str) -> str:
        """
        Преобразование относительной ссылки в абсолютную
        :param url:
        :return:
        """
        if self.host not in url:
            url = self.host + url
        return url


class ProductParserProvider(BsParser):
    """
    Класс для парсинга товара
    """
    def __init__(self, url):
        """
        Конструктор
        :param url:
        """
        self.url = url
        self.data = None


    def to_search(self):
        """
        Формирование словаря для поиска
        :return:
        """
        return {'url': self.asdict()['url']}

    def asdict(self):
        """
        Получение
        :return:
        """
        if not self.data:
            self.data = self.__parse()
        return self.data

    def to_csv(self) -> list:
        """
        Преобразование в массив для сохранение в csv
        :return:
        """
        data = self.asdict()
        return [
            data['title'],
            data['url'],
            data['rate'],
            '|'.join(['%s: %.2f' % (k,v) for k,v in data['params'].items()])
        ]

    def __parse(self):
        """
        Парсинг данных
        :return:
        """
        soup = self._soup(self.url)
        title = soup.select_one('.product-subtitle').text.strip()
        rate = float(soup.select_one('.rating-item.big>.starrating>span').text.strip())
        params = []
        for node in soup.select('.rating-row>.product-rating>.rating-item'):
            if node.select_one('.word-rating'):
                rate = float(node.select_one('.word-rating>span').text.strip())
            else:
                rate = float(node.select_one('.starrating>span').text.strip())
            params.append({
                'name': node.select_one('span').text.strip(),
                'rate': rate
            })

        return {
            'title': title,
            'url': self.url,
            'rate':rate,
            'params': params
        }


# Настройки парсера
PARSER_SETTING = {
    'host': 'https://rskrf.ru',
    'start_url': 'https://rskrf.ru/ratings/produkty-pitaniya/',
    'tree': [
        {
            'type': 'branch',
            'selector': '.categories .category-item a',
            'data': 'html'
        },
        {
            'type': 'branch',
            'selector': '.categories .category-item a',
            'data':'html'
        },
        {
            'type':'leaf',
            'data':'json',
            'selector': r'var data = \{"items":(\[.+\]),"brands"',
            'url_key': 'url'
        }
    ]
}


if __name__ == "__main__":
    try:
        parser = SiteParser(PARSER_SETTING, ProductParserProvider)
        parser.parse()
    except AssertionError:
        print('Error')