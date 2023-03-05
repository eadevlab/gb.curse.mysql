import scrapy
from scrapy.http import HtmlResponse
from scrapy.loader import ItemLoader
from ..items import ProductItem


class DomovoySpider(scrapy.Spider):
    name = "domovoy"
    allowed_domains = ["tddomovoy.ru"]
    start_urls = [
        # "https://tddomovoy.ru/",
        'https://tddomovoy.ru/catalog/posuda/'
    ]
    url = 'https://tddomovoy.ru'

    def parse(self, response: HtmlResponse, **kwargs):
        """
        Парсинг каталога
        :param response:
        :return:
        """
        product_urls = response.xpath("//a[@class='goods-card__title']/@href")
        for product_url in product_urls:
            yield response.follow(product_url, callback=self.parse_product)

        # next = response.xpath('//div[@class="s-goods-list__show-more"]/@data-url').get()
        # if next:
        #     yield response.follow(next, callback=self.parse)

    def parse_product(self, response: HtmlResponse):
        """
        Парсинг товара с использование ItemLoader.
        :param response:
        :return:
        """
        loader = ItemLoader(item=ProductItem(), response=response)
        loader.add_css('_id','.s-card-info__code::text')
        loader.add_xpath('name','//h1//text()')
        loader.add_xpath('price','//div[@itemprop="price"]/@content')
        loader.add_value('url', response.url)
        # loader.add_css('params','.s-card-infos__features-list-item::text')
        loader.add_css('images','.swiper-wrapper .swiper-slide img::attr(data-src)')
        # Характеристики товара
        loader.add_css('tmp_param_names','.s-card-infos__features-list-item .s-card-infos__features-title::text')
        loader.add_css('tmp_param_values','.s-card-infos__features-list-item .s-card-infos__features-text::text')

        yield loader.load_item()


    def __fix_domain(self, url):
        if self.url not in url:
            return self.url + url
        return url
