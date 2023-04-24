import numpy as np
import pandas as pd
from sklearn import preprocessing

class Preprocessor:
    HOME_OWNERSHIP_MAP = {'Own Home': 3, 'Home Mortgage': 2, 'Rent': 1,
                          'Have Mortgage': 2}
    TERM_MAP = {'Short Term': 0, 'Long Term': 1}

    def __init__(self, target):
        self.target = target
        self.medians  = {}
        self.uppers = {}
        self.float_columns = []
        self.le = preprocessing.LabelEncoder()
        self.scaler = preprocessing.StandardScaler()

    def fit(self, dataset):
        self.float_columns = dataset.select_dtypes(include=['float64']).columns

        tmp_ds = dataset.copy()
        for float_column in self.float_columns:
            q1 = np.percentile(dataset[float_column], 25, interpolation='midpoint')
            q3 = np.percentile(dataset[float_column], 75, interpolation='midpoint')
            self.uppers[float_column] = q3 + 1.5 * q1
            self.medians[float_column] = dataset[float_column].median()
            tmp_ds.loc[tmp_ds[float_column] > self.uppers[float_column], float_column] = self.uppers[float_column]

        self.le.fit(tmp_ds['Purpose'])
        self.scaler.fit(dataset[self.float_columns])

    def ballance(self, dataset):
        """Балансировка классов."""
        rat = len(dataset.loc[dataset[self.target] == 0]) // len(dataset.loc[dataset[self.target] == 1])
        ds_1 = dataset.loc[dataset[self.target] == 1]
        ds_1 = ds_1.loc[ds_1.index.repeat(rat)]
        ds_n = pd.concat([dataset.loc[dataset[self.target] == 0], ds_1]).sample(frac=1)
        return ds_n

    def transform(self, dataset):
        """Трансформация."""
        dataset = self.__outliers(dataset)
        dataset = self.__fill(dataset)
        dataset = self.__categories(dataset)
        dataset = self.__new_features(dataset)
        dataset[self.float_columns] = self.scaler.fit_transform(dataset[self.float_columns])

        return dataset

    def fit_transform(self, dataset):
        self.fit(dataset)
        return self.transform(dataset)


    def __fill(self, dataset):
        """Заполнение пропусков."""
        def fix_year(self, row):
            year = row['Years in current job']
            if not year or pd.isnull(year):
                year = '0'
            else:
                year = str(year).replace(' years', '').replace('+','').replace(' year', '')
                if year == '< 1':
                    year = '0'
            row['Years in current job'] = year
            return row

        for col in ['Annual Income', 'Months since last delinquent',
                    'Credit Score', 'Years in current job']:
            dataset[col] = dataset[col].fillna(self.medians[col])

        dataset['Bankruptcies'] = dataset['Bankruptcies'].fillna(0.00)
        dataset['Bankruptcies'] = dataset['Bankruptcies'].astype(np.int)

        dataset = dataset.apply(fix_year, axis=1)
        dataset['Years in current job'] = dataset['Years in current job'].astype(int)
        return dataset

    def __new_features(self, dataset):
        """Добавление новых фич."""
        dataset['ci_ratio'] = dataset['Annual Income'] / dataset['Monthly Debt']
        dataset['max_cr_ratio'] = dataset['Annual Income'] / dataset['Maximum Open Credit']
        return dataset

    def __categories(self, dataset):
        """Обработка категориальных признаков."""
        dataset['Term'] = dataset['Term'].map(self.TERM_MAP)
        dataset['Purpose'] = self.le.transform(dataset['Purpose'])
        dataset['Home Ownership'] = dataset['Home Ownership'].map(self.HOME_OWNERSHIP_MAP)

        return dataset

    def __outliers(self, dataset):
        """Обработка выбросов."""
        for float_column in self.float_columns:
            dataset.loc[dataset[float_column] > self.uppers[float_column], float_column] = self.uppers[float_column]
        return dataset
