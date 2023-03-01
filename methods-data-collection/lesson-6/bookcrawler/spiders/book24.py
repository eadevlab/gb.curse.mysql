import sys

import scrapy
from scrapy.http import HtmlResponse
from ..items import BookcrawlerItem

class Book24Spider(scrapy.Spider):
    name = "book24"
    url = 'https://book24.ru'
    allowed_domains = ["book24.ru"]
    start_urls = ["https://book24.ru/catalog/"]

    def parse(self, response:HtmlResponse, **kwargs):
        """
        Парсинг каталога
        :param response:
        :param kwargs:
        :return:
        """
        books = response.css('.catalog__product-list .product-list__item .product-card__image-link::attr(href)').extract()
        for book_url in books:
            yield response.follow(self.__fix_domain(book_url), callback=self.item_parse)
        next_page = response.css('link[rel="next"]::attr(href)').extract_first()
        if next_page:
            yield response.follow(self.__fix_domain(next_page), callback=self.parse)

    def item_parse(self, response:HtmlResponse):
        """
        Парсинг элемента
        :param response:
        :return:
        """
        price = response.css('[property="product:price:amount"]::attr(content)').extract_first()
        sale_price = None
        if len(response.css('.product-sidebar-price__price-old').extract()) > 0:
            sale_price = price
            price = response.css('.product-sidebar-price__price-old::text')\
                .extract_first().replace('₽','').replace(u'\xa0', u'').strip()

        return BookcrawlerItem(
            title=response.css('h1::text').extract_first().strip(),
            link=response.url,
            source=self.name,
            authors=response.css('[itemprop="author"] meta::attr(content)').extract(),
            price=price,
            sale_price=sale_price,
            rate = response.css('.rating-widget__main-text::text').extract_first().strip()
        )

    def __fix_domain(self, url):
        if self.url not in url:
            return self.url + url
        return url
