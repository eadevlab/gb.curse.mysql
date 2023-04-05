import numpy as np
from sklearn import model_selection
from sklearn.datasets import load_iris
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

class KNN:
    """Класс для классификации методом ближайших соседей."""
    AVAILABLE_WEIGHTS = (None, 'index', 'dist')
    def __init__(self, *, k:int=5, weight:str=None, q:float=0.5):
        """
        Конструктор
        :param k: Количество соседей
        :param weight: Тип определения веса
            - None: без учета весов
            - index: Взвешивание в зависимости от номера соседа
            - dist: Взвешивание относительно расстояния
        :param q: Произвольное число для весов
        """
        self._k = k
        self._q = q
        self._weight = weight
        self._X = None
        self._y = None
        self._classes = None

        assert self._weight in self.AVAILABLE_WEIGHTS
        assert 0 < self._q < 1

    def fit(self, X, y):
        """
        Обучение модели.
        :param X: Фичи
        :param y: Целевое значение
        :return:
        """
        self._X = X
        self._y = y
        self._classes = set(y)

    def predict(self, X):
        """
        Получения классов для входных значений
        :param X:
        :return:
        """
        return [self._point_predict(point) for point in X]

    def _point_predict(self, point):
        """
        Получение класса для точки
        :param point:
        :return:
        """
        neighbors = self._get_neighbors(point)
        counter = {n[0]:0 for n in neighbors}
        if len(counter) == 1:
            # Если все соседи одного класса нет смысла
            return list(counter.keys())[0]
        i = 1
        for cl, dist in neighbors:
            counter[cl] += self._apply_weight(dist, i)
            i += 1
        return max(counter.items(), key=lambda x: x[1])[0]
    def _apply_weight(self, dist, idx):
        """
        Применяем взвешенное голосование
        :param dist: Расстояние
        :param idx: Номер соседа
        :return:
        """
        if self._weight == 'index':
            return self._q**idx
        if self._weight == 'dist':
            return self._q**dist
        return dist

    def _get_neighbors(self, point):
        """
        Получание K ближайших соседей
        :param point:
        :return:
        """
        distances = self._distances(point)
        distances.sort(key=lambda e: e[1])
        return distances[:self._k]

    def _distances(self, point) -> list:
        """
        Расчёт расстояний до каждой точки
        :param point:
        :return:
        """
        return [(self._y[i], self._e_metric(self._X[i], point)) for i in range(len(self._X))]

    def _e_metric(self,p1, p2) -> float:
        """
        Расчёт Евклидовой метрики
        :param p1: Точка 1
        :param p2: Точка 2
        :return: Расстояние между точками
        """
        distance = 0
        for i in range(len(p1)):
            distance += (p1[i] - p2[i]) ** 2
        return np.sqrt(distance)

    @staticmethod
    def accuracy(y_pred, y_test):
        return sum(y_pred == y_test) / len(y_test)


X, y = load_iris(return_X_y=True)
X = X[:, :2]

X_train, X_test, y_train, y_test = model_selection.train_test_split(X, y, test_size=0.2, random_state=1)


model = KNN(k=4)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)

print(model.accuracy(y_pred, y_test))