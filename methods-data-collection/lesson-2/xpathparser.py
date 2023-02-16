from urllib.parse import urlparse

from lxml import html
import requests

class XPathParser:
    """
    Класс для парсинга новостных сайтов с помощью XPath
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; rv:76.0) Gecko/20100101 Firefox/76.0",
        "Pragma":"",
        "Cache-Control":"max-age=0"
    }

    def __init__(self, *, settings:dict, headers=None):
        """
        Конструктор
        :param settings: Настройки парсера
        :param headers: Дополнительные зидеры
        """
        if headers:
            self.headers.update(headers)
        if self.__validate_settings(settings):
            self.settings = settings
        else:
            raise ValueError('Settings err...')
    def __validate_settings(self, settings:dict):
        """
        Валидация настроек
        :return:
        """
        for req in ['params','host','list_xpath']:
            if req not in settings:
                return False
        return True
    def parse(self) -> list:
        """
        Парсинг списка
        :return:
        """
        items = []
        response = requests.get(self.settings['host'], headers=self.headers)
        dom = html.fromstring(response.text)
        print(dom.xpath(self.settings['list_xpath']))
        for el in dom.xpath(self.settings['list_xpath']):
            item = {}
            for param_key, param_xpath in self.settings['params'].items():
                try:
                    item[param_key] = el.xpath(param_xpath)[0]
                except IndexError:
                    continue
            if 'item_url_param' in self.settings:
                if 'add_host' in self.settings and self.settings['add_host']:
                    item[self.settings['item_url_param']] = self.settings['host'] + item[self.settings['item_url_param']].lstrip('/')
                item['source'] = urlparse(item[self.settings['item_url_param']]).netloc
                if item and 'item_params' in self.settings:
                    item.update(self._item_parse(item[self.settings['item_url_param']]))
            items.append(item)
            print(item)
        return items
    def _item_parse(self, url:str) -> dict:
        """
        Парсинг допонительных параметров
        :param url: Ссылка на элемент
        :return:
        """
        result = {}
        response = requests.get(self.settings['host'], headers=self.headers)
        dom = html.fromstring(response.text)
        for param_key, param_xpath in self.settings['item_params'].items():
            try:
                result[param_key] = dom.xpath(param_xpath)[0]
            except IndexError:
                continue
        return result