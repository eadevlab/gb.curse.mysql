"""
Вывод информации о спаршенных вакансиях
"""
import pymongo
from dotenv import dotenv_values
from pymongo import MongoClient
from pprint import pprint


def main_promt():
    """
    Вывод главного меню.
    :return:
    """
    print('Выберете действие')
    print('[1] Вывести 5 последних вакансий для резюме')
    print('[2] Поиск по скилам')
    print('[3] Выход')

def resume_process(collection):
    """
    Поиск вакансий по резюме
    :param collection:
    :return:
    """
    resumes = list(collection.aggregate([
        {"$group":{'_id':"$resume_name"}}
    ]))
    print('Выберете резюме')
    for idx, resume in enumerate(resumes):
        print(f'[{idx+1}] {resume["_id"]}')
    try:
        key = int(input(':= '))
        vacs = collection.find({
            'resume_name': resumes[key-1]['_id']
        }).sort(
            [('posted_date', pymongo.DESCENDING)]).limit(5)
        pprint(list(vacs))
    except (ValueError, IndexError) as e:
        print('Ошибка!')


def search_process(collection):
    """
    Поиск вакансий по скилам
    :param collection:
    :return:
    """
    skill = input('Введите скилл: ')
    vacs = list(collection.find({
        'skills': skill
    }))
    pprint(vacs)

if __name__ == "__main__":
    config = dotenv_values(".env")
    client = MongoClient('localhost', 27017)
    collection = client[config['MONGO_DB']][config['MONGO_COLLECTION']]

    while True:
        main_promt()
        key = input(':= ')
        if key == '1':
            resume_process(collection)
        elif key =='2':
            search_process(collection)
        elif key =='3':
            break
        else:
            print('Неизвестная команда')