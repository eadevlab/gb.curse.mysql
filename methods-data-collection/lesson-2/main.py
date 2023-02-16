import json

from xpathparser import XPathParser

# Настройки парсинга каждого новостного сайта
PARSING_SETTINGS = [
    {
        'host': 'https://news.mail.ru/',
        'add_host': False,
        'item_url_param':'url',
        'list_xpath': '//div[@data-logger="news__MainPopularNews"]//div[contains(@class,"cols__column")]',
        'params': {
            'title':'./div//a/span/text()',
            'url':'./div//a/@href',
        },
        'item_params': {
            'published': '//span[@datetime]/@datetime'
        }
    },
    {
        'host': 'https://lenta.ru/',
        'add_host': True,
        'item_url_param':'url',
        'list_xpath': '//div[contains(@class,"last24")]/a',
        'params': {
            'title':'./div/span/text()',
            'url':'@href',
        },
        'item_params': {
            'published': '//a[contains(@class,"topic-header__time")]/text()'
        }
    },

]

result = []
for settings in PARSING_SETTINGS:
    result += XPathParser(settings=settings).parse()

with open('./news.json', 'w') as f:
    json.dump(result, f)
