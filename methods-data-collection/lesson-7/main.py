from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
from leruacrawler import settings
from leruacrawler.spiders.domovoy import DomovoySpider

if __name__ == "__main__":
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)
    process = CrawlerProcess(settings=crawler_settings)
    process.crawl(DomovoySpider)
    process.start()
