from dotenv import dotenv_values, set_key
from collections import OrderedDict
import getpass
from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
from crawler import settings
from crawler.spiders.hh import HhSpider


def str_input(prompt, default=''):
    """
    Ввод данных типа str
    :param prompt:
    :return:
    """
    return typed_input(prompt, str, default)

def typed_input(prompt, input_type, default=''):
    """
    Типизированный ввод данных
    :param default:
    :param prompt:
    :param input_type:
    :return:
    """
    value = None
    while True:
        try:
            value = input_type(input(prompt))
        except ValueError:
            print('Ошибка ввода')
            continue
        break
    return value if value else default

def create_project_dotenv(env_file_path:str) -> OrderedDict:
    """
    Генерация файла настроек
    :param env_file_path: Путь к файлу .env
    :return: Настройки
    """
    config = OrderedDict(
        HH_EMAIL=str_input('Введите email пользователя: '),
        HH_PASSWORD=getpass.getpass('Введите пароль пользователя: '),
        MONGO_DB=str_input('Введите название базы данных mongodb[parser_db]: ','parser_db'),
        MONGO_COLLECTION=str_input('Введите название коллекции mongodb[users]: ','users')
    )
    for key, value in config.items():
        set_key(env_file_path, key, value)

    return config

if __name__ == "__main__":
    # Загружаем настройки из файла .env
    config = dotenv_values(".env")
    if not config:  # если настроек нет их необходимо создать
        config = create_project_dotenv(".env")

    crawler_settings = Settings()
    crawler_settings.setmodule(settings)
    process = CrawlerProcess(settings=crawler_settings)
    process.crawl(HhSpider,
                db_name=config['MONGO_DB'],
                collection=config['MONGO_COLLECTION'],
                login=config['HH_EMAIL'],
                password=config['HH_PASSWORD'],
    )
    process.start()
