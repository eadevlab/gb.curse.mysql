import sys

from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
from bookcrawler import settings
from bookcrawler.spiders.book24 import Book24Spider
from bookcrawler.spiders.labirint import LabirintSpider

if __name__ == "__main__":
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)

    try:
        spider_name = sys.argv[1]
        process = CrawlerProcess(settings=crawler_settings)

        if spider_name == 'book24':
            process.crawl(Book24Spider)
        elif spider_name == 'labirint':
            process.crawl(LabirintSpider)
        process.start()

    except IndexError:
        print('Ошибка запуска')
