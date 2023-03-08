import datetime
import json
import os.path

import scrapy
from scrapy.http import HtmlResponse
from ..items import CrawlerItem


class HhSpider(scrapy.Spider):
    name = "hh"
    allowed_domains = ["hh.ru"]
    start_urls = []
    login_endpoint = "https://hh.ru/account/login"
    url = "https://hh.ru"

    def __init__(self, **kwargs):
        """Конструктор."""
        super().__init__()
        self.db_name = kwargs.get('db_name')
        self.collection = kwargs.get('collection')
        self.login = kwargs.get('login')
        self.password = kwargs.get('password')
        self.start_urls.append(self.login_endpoint)


    def parse(self, response:HtmlResponse):
        """Авторизация."""
        xsrf_token = response.css('input[name="_xsrf"]::attr(value)').extract_first()
        yield scrapy.FormRequest(
            self.login_endpoint,
            method='POST',
            callback=self.after_login,
            formdata={
                'username': self.login,
                'password': self.password,
                '_xsrf': xsrf_token,
                'accountType': 'EMPLOYER',
                'backUrl': 'https://hh.ru/',
                'failUrl': '/account/login?backurl=%2F',
                'loginAs':'',
                'remember': 'yes',
                # 'isBot': 0
            },
            headers={
                'x-xsrftoken': xsrf_token,
                'x-hhtmsource': 'account_login',
                'x-requested-with': 'XMLHttpRequest'
            }
        )


    def after_login(self, response:HtmlResponse):
        """Переход на страницу списка резюме."""
        yield response.follow('https://hh.ru/applicant/resumes',callback=self.fetch_resumes)


    def fetch_resumes(self, response:HtmlResponse):
        """
        Получение ссылок на подходящие вакансии к резюме пользователя
        :param response:
        :return:
        """
        for resume_node in response.css('div[data-qa="resume"]'):
            resume_link = resume_node.css('.applicant-resumes-recommendations-button a[data-qa="resume-recommendations__button_updateResume"]::attr(href)').extract_first()
            if resume_link:
                    yield response.follow(self.__fix_domain(resume_link),
                                      callback=self.parse_vacancies,
                                      cb_kwargs={
                                          'resume_title': resume_node.attrib['data-qa-title'],
                                          'resume_id': resume_node.attrib['data-qa-id'],
                                      })


    def parse_vacancies(self, response:HtmlResponse, **kwargs):
        """Парсинг списка вакансий."""
        vacancy_links = response.css('.serp-item__title::attr(href)')
        for vacancy_link in vacancy_links:
            if vacancy_link:
                yield response.follow(
                    vacancy_link,
                    callback=self.parse_vacancy,
                    cb_kwargs=kwargs
                )


    def parse_vacancy(self, response:HtmlResponse, **kwargs):
        """Парсинг вакансии."""

        params = {
            '_id': os.path.basename(response.url.split('?')[0]),
            'title': response.css('h1::text').extract_first().strip(),
            'min_salary': None,
            'max_salary': None,
            'short': "\n".join(response.css('.vacancy-description-list-item::text').extract()),
            'skills': [_.strip() for _ in response.css('.bloko-tag__section_text::text').extract()],
            'posted_date': None,
            'resume_id': kwargs.get('resume_id'),
            'resume_name': kwargs.get('resume_title'),
        }
        # Данные о зп проще всего спарсить из метрики json ld
        page_json = json.loads(response.xpath('//script[@type="application/ld+json"]//text()').extract_first())
        if 'baseSalary' in page_json:
            if 'value' in page_json['baseSalary']:
                if 'minValue' in page_json['baseSalary']['value']:
                    params['min_salary'] = float(page_json['baseSalary']['value']['minValue'])
                if 'maxValue' in page_json['baseSalary']['value']:
                    params['max_salary'] = float(page_json['baseSalary']['value']['maxValue'])

        if 'datePosted' in page_json:
            params['posted_date'] = datetime.datetime.strptime(page_json['datePosted'],'%Y-%m-%dT%H:%M:%S.%f%z')
        yield CrawlerItem(**params)


    def __fix_domain(self, url):
        """
        Добавление домена к ссылке
        :param url:
        :return:
        """
        if url and self.url not in url:
            return self.url + url
        return url
