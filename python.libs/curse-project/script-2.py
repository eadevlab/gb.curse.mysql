import datetime
import sys

import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
from sklearn import preprocessing
from preprocessor import Preprocessor

ds = pd.read_csv('./train.csv')

# price_corr = ds.corr().abs()
# price_corr = price_corr.unstack().sort_values()['Price']
#
# plt.figure(figsize = (16, 8))
# plt.bar(list(price_corr.keys())[:-1], list(price_corr)[:-1])
# plt.xticks(rotation=90)
# plt.show()

# print(ds.head())

prep = Preprocessor()
prep.fit(ds)
ds = prep.transform(ds)

price_corr = ds.corr().abs()
price_corr = price_corr.unstack().sort_values()['Price']

plt.figure(figsize = (16, 8))
plt.bar(list(price_corr.keys())[:-1], list(price_corr)[:-1])
plt.xticks(rotation=90)
plt.show()

sys.exit()
# Тестируемс
from sklearn.model_selection import train_test_split, cross_val_score

TARGET = 'Price'

# object_fields = list(ds.select_dtypes(include='object').columns)
# encoders = {}
# for field in object_fields:
#     encoders[field] = preprocessing.LabelEncoder()
#     encoders[field].fit(ds[field])
#     ds[field] = encoders[field].transform(ds[field])

# ds['LifeSquare'] = ds['LifeSquare'].fillna(0)
# ds['Healthcare_1'] = ds['Healthcare_1'].fillna(0)

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

best_params = {'n_estimators': 700, 'min_samples_split': 12, 'min_samples_leaf': 2, 'max_features': 'sqrt', 'max_depth': 13, 'bootstrap': False}

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
