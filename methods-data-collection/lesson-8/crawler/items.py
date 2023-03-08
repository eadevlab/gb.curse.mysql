import scrapy

class CrawlerItem(scrapy.Item):
    _id = scrapy.Field()  # Идентификатор вакансии
    title = scrapy.Field()  # Название вакансии
    posted_date = scrapy.Field()  # Дата публикации
    min_salary = scrapy.Field()  # Минимальная зп
    max_salary = scrapy.Field()  # Максимальная зп
    short = scrapy.Field()  # Краткое описание
    skills = scrapy.Field()  # Ключевые скиллы
    resume_id = scrapy.Field()  # Идентификатор резюме
    resume_name = scrapy.Field()  # Название резюме