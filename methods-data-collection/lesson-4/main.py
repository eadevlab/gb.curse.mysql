from scrapper import ParserStorage, DB_NAME, TABLE_NAME
import pandas as pd

def float_input(prompt):
    """
    Ввод данных типа float
    :param prompt:
    :return:
    """
    return typed_input(prompt, float)

def typed_input(prompt, input_type):
    """
    Типизированный ввод данных
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
    return value

def search_products(min_rate: float):
    """
    Поиск товаров по рейтингу и вывод ввиде таблицы
    :param min_rate:
    :return:
    """
    storage = ParserStorage(DB_NAME, TABLE_NAME)
    items = storage.find({'rate':{'$gte':min_rate},'params':{'name':'Качество','rate':min_rate}},'-rate')
    print(
        pd.DataFrame.from_records(items)
    )


if __name__ == "__main__":
    search_products(
        float_input('Введите минимальный рейтинг: ')
    )