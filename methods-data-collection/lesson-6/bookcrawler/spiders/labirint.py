import sys

import scrapy
from scrapy.http import HtmlResponse
from ..items import BookcrawlerItem

class LabirintSpider(scrapy.Spider):
    name = "labitint"
    url = 'https://labirint.ru'
    allowed_domains = ["labirint.ru"]
    start_urls = ["https://labirint.ru/books/"]

    def parse(self, response:HtmlResponse, **kwargs):
        """
        Парсинг каталога
        :param response:
        :param kwargs:
        :return:
        """
        books = response.css('#catalog .genres-carousel__item a.cover::attr(href)').extract()
        for book_url in books:
            yield response.follow(self.__fix_domain(book_url), callback=self.item_parse)
        next_page = response.css('.pagination-next__text::attr(href)').extract_first()
        if next_page:
            yield response.follow(self.start_urls[0]+next_page, callback=self.parse)

    def item_parse(self, response:HtmlResponse):
        """
        Парсинг элемента
        :param response:
        :return:
        """
        price = response.css('.buying-price-val-number::text').extract_first()
        if not price:
            price = response.css('.buying-priceold-val-number::text').extract_first()
        sale_price = response.css('.buying-pricenew-val-number::text').extract_first()
        return BookcrawlerItem(
            title=response.css('h1::text').extract_first().strip(),
            link=response.url,
            source=self.name,
            authors=response.css('.authors a::text').extract(),
            price=price,
            sale_price=sale_price,
            rate=response.css('#rate::text').extract_first().strip()
        )

    def __fix_domain(self, url):
        if self.url not in url:
            return self.url + url
        return url
