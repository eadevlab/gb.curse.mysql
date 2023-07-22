import pandas as pd
from sklearn import preprocessing
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.pipeline import FeatureUnion
from joblib import dump
from conf.dicts import CATEGORICAL_FEATURES_MAPS
from conf.pipes import ColumnSelector, CategoryTransform
pd.options.mode.chained_assignment = None
import os

curdir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

dataset = pd.read_csv(os.path.join(root_dir,'bank.csv'), delimiter=';')

TARGET = 'y'

dataset['y'] = dataset['y'].map({'no':0, 'yes': 1})
dataset['y'] = dataset['y'].astype(int)

categorical_columns = [col for col in dataset.columns if dataset[col].dtype=="O"]

rat = len(dataset.loc[dataset[TARGET]==0])//len(dataset.loc[dataset[TARGET]==1])
ds_1 = dataset.loc[dataset[TARGET]==1]
ds_1 = ds_1.loc[ds_1.index.repeat(rat)]

dataset_normalize = pd.concat([dataset.loc[dataset[TARGET]==0], ds_1]).sample(frac=1)


other_cols = dataset_normalize.columns.difference(categorical_columns).difference(['balance','duration','y'])


transformers = list()
transformers.append(('cats', Pipeline([
    ('selector', ColumnSelector(columns=categorical_columns)),
    ('scaler', CategoryTransform(map=CATEGORICAL_FEATURES_MAPS)),
])))

transformers.append(('num', Pipeline([
    ('selector', ColumnSelector(columns=['balance','duration'])),
    ('scaler', preprocessing.MinMaxScaler())
])))

transformers.append(('other', Pipeline([
    ('selector', ColumnSelector(columns=other_cols)),
])))

feats = FeatureUnion(transformers)

classifier = Pipeline([
    ('features',feats),
    ('classifier', RandomForestClassifier(random_state=42))
])

classifier.fit(dataset_normalize.drop(TARGET, axis=1), dataset_normalize[TARGET])


dump(classifier, os.path.join(curdir, 'models','bank_model.joblib'))