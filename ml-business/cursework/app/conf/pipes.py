from sklearn.base import BaseEstimator, TransformerMixin

class FeatureSelector(BaseEstimator, TransformerMixin):
    def __init__(self, column):
        self.column = column

    def fit(self, X, y=None):
        return self

    def transform(self, X, y=None):
        return X[self.column]

class ColumnSelector(BaseEstimator, TransformerMixin):
    def __init__(self, columns):
        self.columns = columns

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        return X[self.columns]

class CategoryTransform(BaseEstimator, TransformerMixin):
    def __init__(self, map):
        self.map = map

    def fit(self, X, y=None):
        return self

    def transform(self, X, y=None):
        for _ in self.map.keys():
            X[_] = X[_].map(self.map[_])
        return X