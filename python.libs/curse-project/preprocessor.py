import datetime
import math
import sys

import numpy as np
import pandas as pd
from sklearn.decomposition import PCA


class Preprocessor:
    """
    Класс для предобработки датафрэима.
    """
    def __init__(self):
        """
        Конструктор.
        """
        self.current_year = datetime.datetime.now().year
        self.districts_rate = None
        self.medians = None
        self.districts_price_per_meter = None
        self.minmax = {
            'KitchenSquare': (),
            'HouseFloor': (),
            'Rooms': (),
            'LifeSquare': (),
            'Square': ()
        }
        self.house_floor_means = None
        self.districts_healthcare_1 = None
        self.healthcare_mean = None
        self.room_median_square = None  # средняя площадь комнаты
        self.pca = PCA(n_components=1, random_state=42)

    def fit(self, dataset: pd.DataFrame):
        """
        Расчет средних и медианных значений
        :param dataset:
        :return:
        """
        self.medians = dataset.groupby(['DistrictId']).agg(
            hf_median=('HouseFloor', np.median),
            lq_median=('LifeSquare', np.median),
            kq_median=('KitchenSquare', np.median),
            rooms_median=('Rooms', np.median)
        ).reset_index()
        self.house_floor_means = dataset.groupby('HouseYear').agg(
            hf_median=('HouseFloor', np.median),
            hf_min=('HouseFloor', np.min),
            hf_max=('HouseFloor', np.max)
        ).reset_index()

        self.districts_healthcare_1 = dataset.groupby(['DistrictId'])[
            'Healthcare_1'].agg('mean').to_dict()
        self.healthcare_mean = dataset['Healthcare_1'].mean()
        self.room_median_square = round(dataset['LifeSquare'].median()/dataset['Rooms'].median(),2)

        self.pca.fit(dataset[['Social_1','Social_2','Social_3']])

        self.districts_price_per_meter = (dataset.groupby(['DistrictId'])['Price'].agg('median') \
                                         / dataset.groupby(['DistrictId'])['Square'].agg('median')).to_dict()

        self.districts_rate = dict(dataset['DistrictId'].value_counts()/dataset.shape[0])
    def __fixes(self, dataset: pd.DataFrame) -> pd.DataFrame:
        """
        Фиксы датафрэима.
        :param dataset: Исходный датасет
        :return: pd.DataFrame
        """
        def fix_square(row):
            """
            Фикс общей площади
            :param row:
            :return: pd.Series
            """
            if row['Square'] < row['LifeSquare'] + row['KitchenSquare']:
                # Общая площадь не может быть меньше суммы площадей жилой и кухни
                row['Square'] = row['LifeSquare'] + row['KitchenSquare']
            return row

        def fix_house_year(row):
            """
            Фикс года постройки дома
            :param row:
            :return: pd.Series
            """
            house_year = row['HouseYear']
            try:
                house_year = datetime.datetime.strptime(str(int(house_year)), '%Y%d%m').year
            except ValueError:
                house_year = datetime.datetime.now().year

            row['HouseYear'] = house_year
            return row

        dataset = dataset.apply(fix_house_year, axis=1)
        dataset = dataset.apply(fix_square, axis=1)

        dataset.loc[(dataset['Rooms']==0)|(dataset['Rooms']>6),'Rooms'] = round(dataset.loc[
            (dataset['Rooms']==0)|(dataset['Rooms']>6),'LifeSquare']/self.room_median_square)
        dataset.loc[dataset['Rooms']==0,'Rooms'] = 1
        return dataset

    def __fillna(self, dataset: pd.DataFrame) -> pd.DataFrame:
        """
        Заполнение пропуской
        :param dataset: Исходный датафрэим
        :return: pd.DataFrame
        """
        def fill_house_floor(row):
            """
            Заполнение этажа
            :param row:
            :return: pd.Series
            """
            row['HouseFloor'] = float(
                self.house_floor_means.loc[self.house_floor_means['HouseYear'] == row['HouseYear']]['hf_median'])
            return row


        dataset.loc[dataset['Healthcare_1'].isna(), 'Healthcare_1'] = dataset['DistrictId'].map(self.districts_healthcare_1)
        # Те что не получилось заполнить по районам заполним средним значением
        dataset['Healthcare_1'].fillna(self.healthcare_mean, inplace=True)

        dataset.loc[dataset['HouseFloor'] < 2] = dataset.loc[dataset['HouseFloor'] < 2].apply(fill_house_floor, axis=1)
        # Вычислим соотношение остальной площади от общей площади
        other_koef = round((dataset['Square'] - dataset['KitchenSquare'] - dataset['LifeSquare']).median() / dataset['Square'].median(),3)
        # Заполнение пустой жилой площади
        dataset['LifeSquare'].fillna((dataset['Square']-dataset['KitchenSquare']-dataset['Square']*other_koef),inplace=True)
        # Заполнение пропусков комнат
        # dataset['Rooms'].fillna(self.medians[dataset['DistrictId']]['rooms_median'], inplace=True)
        # print(self.medians.loc(self.medians['DistrictId']==dataset['DistrictId'])['rooms_median'])
        return dataset

    def __new_featrures(self, dataset: pd.DataFrame) -> pd.DataFrame:
        """
        Добавление новых свойств.
        :param dataset:
        :return: ps.DataFrame
        """
        dataset['Social'] = self.pca.transform(dataset[['Social_1','Social_2','Social_3']])
        dataset['PPM'] = dataset['DistrictId'].map(self.districts_price_per_meter)
        dataset['District_rate'] = dataset['DistrictId'].map(self.districts_rate)

        return dataset

    def transform(self, dataset: pd.DataFrame) -> pd.DataFrame:
        """
        Трансформирование датафрэима
        :param dataset:
        :return: pd.DataFrame
        """
        dataset = self.__fillna(dataset)
        dataset = self.__fixes(dataset)

        dataset.replace({'Ecology_2': {'A': 0, 'B': 1}}, inplace=True)
        dataset.replace({'Ecology_3': {'A': 0, 'B': 1}}, inplace=True)
        dataset.replace({'Shops_2': {'A': 0, 'B': 1}}, inplace=True)

        dataset = self.__new_featrures(dataset)

        # удаляем лишние поля
        dataset = dataset.drop(['Social_1', 'Social_2', 'Social_3', 'Ecology_2', 'Ecology_3', 'Id'], axis=1)

        return dataset
