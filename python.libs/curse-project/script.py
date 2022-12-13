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

object_fields = list(ds.select_dtypes(include='object').columns)
encoders = {}
for field in object_fields:
    encoders[field] = preprocessing.LabelEncoder()
    encoders[field].fit(ds[field])
    ds[field] = encoders[field].transform(ds[field])

# print(ds['HouseFloor'])

# FIX ROOOMS
rooms_min_max_sq = ds.loc[(ds['Rooms'] <= 6) & (ds['Rooms'] > 0)].groupby('Rooms').agg(
    min_sq=('Square', np.min),
    max_sq=('Square', np.max),
    med_sq=('Square', np.median)
).sort_values('Rooms', ascending=False).reset_index()


def fix_rooms(row):
    row['Rooms'] = rooms_min_max_sq.loc[
        (row['Square'] > rooms_min_max_sq['min_sq']) & (row['Square'] < rooms_min_max_sq['max_sq'])].iloc[0]['Rooms']
    return row


bad_rooms_index = list(ds.loc[ds['Rooms'] > 6].index) + list(ds.loc[ds['Rooms'] == 0].index)
# print(ds.loc[bad_rooms_index].apply(fix_rooms, axis=1))
ds.loc[bad_rooms_index] = ds.loc[bad_rooms_index].apply(fix_rooms, axis=1)


# END FIX ROOMS


# Года постройки больше текущего
# print(ds.loc[(ds['HouseYear'] > 2022), 'HouseYear'])


def fix_house_year(row):
    house_year = row['HouseYear']
    try:
        house_year = datetime.datetime.strptime(str(int(house_year)), '%Y%d%m').year
    except ValueError:
        house_year = datetime.datetime.now().year

    row['HouseYear'] = house_year
    return row


ds.loc[ds['HouseYear'] > 2022] = ds.loc[ds['HouseYear'] > 2022].apply(fix_house_year, axis=1)
# print(ds.loc[ds['HouseYear'] > 2022].apply(fix_house_year, axis=1)['HouseYear'])


# ds.loc[ds['Square']<ds['LifeSquare']+ds['KitchenSquare']]
# ds.loc[ds['Square']<ds['LifeSquare']]
# ds.loc[ds['Floor']>ds['HouseFloor']]
# ds.loc[ds['HouseFloor']<2]
medians = ds.groupby(['HouseYear']).agg(
    hf_median=('HouseFloor', np.median),
    lq_median=('LifeSquare', np.median),
    kq_median=('KitchenSquare', np.median)
).reset_index()


# print(medians)

# print(ds.loc[ds['KitchenSquare'] < 1])
# print(ds.loc[ds['LifeSquare'] < ds['KitchenSquare']])
# print(ds.loc[ds['LifeSquare'].isnull()])

# Не может быть общая площадь меньше площади кухни + жилой
# print(ds.loc[ds['Square']<ds['LifeSquare']+ds['KitchenSquare']])
def fix_square(row):
    if row['Square'] < row['LifeSquare'] + row['KitchenSquare']:
        row['Square'] = row['LifeSquare'] + row['KitchenSquare']
    return row


ds.loc[ds['Square'] < ds['LifeSquare'] + ds['KitchenSquare']] = ds.loc[
    ds['Square'] < ds['LifeSquare'] + ds['KitchenSquare']].apply(fix_square, axis=1)

TARGET = 'Price'
ds = ds.drop(['Ecology_2', 'Ecology_3', 'Id'], axis=1)

object_fields = list(ds.select_dtypes(include='object').columns)
encoders = {}
for field in object_fields:
    encoders[field] = preprocessing.LabelEncoder()
    encoders[field].fit(ds[field])
    ds[field] = encoders[field].transform(ds[field])

ds['LifeSquare'] = ds['LifeSquare'].fillna(0)
ds['Healthcare_1'] = ds['Healthcare_1'].fillna(0)

# print(ds.loc
# [ds['LifeSquare'].isnull()])
# print(ds.head())
# sys.exit()
y = ds[TARGET]
X = ds.drop([TARGET], axis=1)
# min max scaller
scaler = preprocessing.MinMaxScaler()
X[X.select_dtypes(include='float').columns] = scaler.fit_transform(X[X.select_dtypes(include='float').columns])

from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, shuffle=True)
# print(pd.value_counts(y.values.ravel()))
from sklearn.linear_model import LinearRegression, LogisticRegression, ARDRegression, HuberRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix, plot_confusion_matrix
from sklearn.metrics import r2_score, mean_squared_error, accuracy_score

# n_estimators = [50, 100, 200, 300, 500]
# max_features = ["auto", "sqrt", "log2"]
# max_depth = [3, 6]
#
# estimator = GradientBoostingRegressor()
# parameters = {
#     "learning_rate": [0.01, 0.025, 0.05, 0.075, 0.1, 0.15, 0.2],
#     "min_samples_split": np.linspace(0.1, 0.5, 12),
#     "min_samples_leaf": np.linspace(0.1, 0.5, 12),
#     "max_depth":[3,5,8],
#     "criterion": ["friedman_mse",  "mae"],
#     "subsample":[0.5, 0.618, 0.8, 0.85, 0.9, 0.95, 1.0],
#     "n_estimators":[10]
#     }
# grid = GridSearchCV(estimator, param_grid=parameters, n_jobs=-1, cv=5)
# grid.fit(X_train, y_train)
#
# print(grid.best_score_ , grid.best_params_)
# sys.exit()

for model in [
    # LinearRegression(),
    # LogisticRegression(),
    # ARDRegression(),
    # DecisionTreeRegressor(),
    RandomForestRegressor(),
    GradientBoostingRegressor(),
    GradientBoostingRegressor( learning_rate=0.2, max_depth=8, min_samples_leaf=0.1, min_samples_split=0.17272727272727273,n_estimators=10,subsample=0.95)
]:
    print(type(model).__name__)
    print('-' * 10)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    rmse = mean_squared_error(y_test, y_pred, squared=False)
    r2 = r2_score(y_test, y_pred)
    # act = accuracy_score(y_test, predict_test)
    print(
        f'MSE:{round(mse, 5)}\n'
        f'R2:{round(r2, 5)}\n'
        f'RMSE:{round(rmse, 5)}\n'
    )
    # print(accuracy_score(y_test, y_pred))
    # print(f"accuracy:   {accuracy_score(y_test, y_pred)}")
    # print(classification_report(y_test, y_pred))
    print('-' * 10)


# Result class
class Preparer:
    """
    Класс для предобработки датафрэима.
    """
    def __fixes(self, ds: pd.DataFrame) -> pd.DataFrame:
        """
        Различные исправления датасета, запонение пропусков
        :param ds: Исходный датасет
        :return: pd.DataFrame
        """
        def fix_square(row):
            """
            Фикс общей площади
            :param row:
            :return: pd.Series
            """
            if row['Square'] < row['LifeSquare'] + row['KitchenSquare']:
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

        def fix_rooms(row):
            """
            Фикс количества комнат
            :param row:
            :return:
            """
            row['Rooms'] = rooms_min_max_sq.loc[
                (row['Square'] > rooms_min_max_sq['min_sq']) & (row['Square'] < rooms_min_max_sq['max_sq'])].iloc[0][
                'Rooms']
            return row
        rooms_min_max_sq = ds.loc[(ds['Rooms'] <= 6) & (ds['Rooms'] > 0)].groupby('Rooms').agg(
            min_sq=('Square', np.min),
            max_sq=('Square', np.max),
            med_sq=('Square', np.median)
        ).sort_values('Rooms', ascending=False).reset_index()

        return ds

    def transform(self, ds: pd.DataFrame) -> pd.DataFrame:
        """
        Трансвормирование датасета
        :param ds:
        :return: pd.DataFrame
        """
        return ds
