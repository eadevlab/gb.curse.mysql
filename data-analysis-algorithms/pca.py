import numpy as np
from sklearn import model_selection
from sklearn.datasets import load_iris


class SingPCA:
    """Класс метода главных компонент с использование сингулярного разложения."""
    def __init__(self, n_components: int=None):
        """
        Конструктор
        int n_components: Количество компонент
            - default: All
        """
        self.n_components = n_components
        self._w = []

    def fit(self, X):
        """
        Нахождение матрицы весов
        :param X:
        :return:
        """
        if not self.n_components:
            self.n_components = X.shape[1]
        X_centered = self._centering(X)
        p, d, q = np.linalg.svd(X_centered, full_matrices=False)
        self._w = q.T[:,:self.n_components]
        # test = p[:, :self.n_components]*d[:self.n_components]
        # print(self.transform(X)[0])
        # print(test[0])

    def _centering(self, X):
        """
        Центрирование матрицы признаков
        np.array X: Матрица признаков
        np.array Центрированная матрица признаков
        """
        return (X - np.mean(X, axis=0)) / np.std(X, axis=0)

    def transform(self, X):
        """
        Трансформирование исходной матрицы
        :param X:
        :return:
        """
        return self._centering(X) @ self._w

    def fit_transform(self, X):
        self.fit(X)
        return self.transform(X)


X, y = load_iris(return_X_y=True)

spca = SingPCA(3)
spca.fit(X)
X = spca.transform(X)
