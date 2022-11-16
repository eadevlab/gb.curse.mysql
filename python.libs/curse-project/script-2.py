import datetime
import sys

import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
from sklearn import preprocessing

ds = pd.read_csv('./train.csv')


# print(ds.head())

class Preprocessor:
    def __init__(self):
        self.current_year = datetime.datetime.now().year
        self.districtsRate = None
        self.medians = None
        self.districtsPricePerMeter = None
        self.minmax = {
            'KitchenSquare': (),
            'HouseFloor': (),
            'Rooms': (),
            'LifeSquare': (),
            'Square': ()
        }
        self.houseFloorMeans = None

    def fit(self, dataset: pd.DataFrame):
        self.medians = dataset.groupby(['DistrictId']).agg(
            hf_median=('HouseFloor', np.median),
            lq_median=('LifeSquare', np.median),
            kq_median=('KitchenSquare', np.median)
        ).reset_index()
        self.houseFloorMeans = dataset.groupby('HouseYear').agg(
            hf_median=('HouseFloor', np.median),
            hf_min=('HouseFloor', np.min),
            hf_max=('HouseFloor', np.max)
        ).reset_index()

    def __fixes(self, dataset: pd.DataFrame) -> pd.DataFrame:
        def fix_square(row):
            if row['Square'] < row['LifeSquare'] + row['KitchenSquare']:
                row['Square'] = row['LifeSquare'] + row['KitchenSquare']
            return row

        def fix_house_year(row):
            house_year = row['HouseYear']
            try:
                house_year = datetime.datetime.strptime(str(int(house_year)), '%Y%d%m').year
            except ValueError:
                house_year = datetime.datetime.now().year

            row['HouseYear'] = house_year
            return row

        # def fix_rooms(row):
        #     row['Rooms'] = rooms_min_max_sq.loc[
        #         (row['Square'] > rooms_min_max_sq['min_sq']) & (row['Square'] < rooms_min_max_sq['max_sq'])].iloc[0][
        #         'Rooms']
        #     return row
        dataset = dataset.apply(fix_house_year, axis=1)
        dataset = dataset.apply(fix_square, axis=1)
        return dataset

    def __fillna(self, dataset: pd.DataFrame) -> pd.DataFrame:
        def fill_house_floor(row):
            row['HouseFloor'] = float(
                self.houseFloorMeans.loc[self.houseFloorMeans['HouseYear'] == row['HouseYear']]['hf_median'])
            return row

        dataset.loc[dataset['HouseFloor'] < 2] = dataset.loc[dataset['HouseFloor'] < 2].apply(fill_house_floor, axis=1)
        return dataset

    def __new_featrures(self, dataset: pd.DataFrame) -> pd.DataFrame:
        return dataset

    def transform(self, dataset: pd.DataFrame) -> pd.DataFrame:
        # удаляем лишние поля
        dataset = dataset.drop(['Ecology_2', 'Ecology_3', 'Id'], axis=1)

        dataset = self.__fillna(dataset)
        dataset = self.__fixes(dataset)
        dataset = self.__new_featrures(dataset)
        return dataset


prep = Preprocessor()
prep.fit(ds)
ds = prep.transform(ds)

# Тестируемс
from sklearn.model_selection import train_test_split, cross_val_score

TARGET = 'Price'

object_fields = list(ds.select_dtypes(include='object').columns)
encoders = {}
for field in object_fields:
    encoders[field] = preprocessing.LabelEncoder()
    encoders[field].fit(ds[field])
    ds[field] = encoders[field].transform(ds[field])

ds['LifeSquare'] = ds['LifeSquare'].fillna(0)
ds['Healthcare_1'] = ds['Healthcare_1'].fillna(0)

# ds['Price'] = ds['Price']*1000000
# ds['Price'] = ds['Price'].astype(int)
# print(ds.info())
y = ds[TARGET]
X = ds.drop([TARGET], axis=1)

# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, shuffle=True)

from sklearn.linear_model import RANSACRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.model_selection import KFold
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import GridSearchCV

best_params = {'max_depth': 16, 'max_features': 'sqrt', 'min_samples_split': 2, 'n_estimators': 256}
model = RandomForestRegressor(**best_params)
model.fit(X, y)
y_pred = model.predict(X)
print(y_pred[:5])
print(y[:5])

cv_score = cross_val_score(
    model,
    X,
    y,
    scoring='r2',
    cv=KFold(
        n_splits=5,
        shuffle=True,
        random_state=42
    )
)
print(f'R2: {round(cv_score.mean(), 3)}')
