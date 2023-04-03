from sklearn import model_selection
from sklearn.tree import DecisionTreeRegressor
from sklearn.datasets import load_diabetes
import numpy as np

class Boosting:
    def __init__(self, *, max_depth=1, eta=0.1, random_state=42, n_estimators=3):
        """
        Конструктор.
        :param max_depth: Максимальная глубина дерева
        :param eta: Скорость обучения
        :param random_state:
        :param n_estimators: Количество деревьев
        """
        self.trees = []
        self._max_depth = max_depth
        self._eta = eta
        self._random_state = random_state
        self._n_estimators = n_estimators

        self._train_errors = []
        self._test_errors = []


    def fit(self, X_train, y_train, X_test, y_test):
        """
        Обучение модели.
        :param X_train: Фичи (трэин)
        :param y_train: Таргет (трэин)
        :param X_test: Фичи (тест)
        :param y_test: Таргет (тест)
        :return:
        """
        for i in range(self._n_estimators):
            current_tree = DecisionTreeRegressor(max_depth=self._max_depth, random_state=self._random_state)
            target = self._target(X_train, y_train)
            current_tree.fit(X_train, target)
            self.trees.append(current_tree)

            self._train_errors.append(
                self._mse(y_train, self.predict(X_train))
            )
            self._test_errors.append(
                self._mse(y_test, self.predict(X_test))
            )

    def predict(self, rows):
        """Предсказание."""
        return np.array(sum([tree.predict(rows)*self._eta for tree in self.trees]))

    def _target(self, rows, y):
        """Получение значений целевой переменной."""
        if len(self.trees) == 0:
            return y
        return self._residual(y, self.predict(rows))


    def _residual(self, y:float, z:float) -> float:
        return - (z - y)

    def _mse(self, real, predicted) -> float:
        """Получение ошибки."""
        return sum((real-predicted)**2)/ len(real)

    def get_train_errors(self):
        return self._train_errors

    def get_test_errors(self):
        return self._test_errors


    def get_test_mse(self):
        return self._test_errors[-1] if len(self._train_errors) else 0

    def get_train_mse(self):
        return self._train_errors[-1] if len(self._train_errors) else 0


X, y = load_diabetes(return_X_y=True)
X, y = X[:10], y[:10]

X_train, X_test, y_train, y_test = model_selection.train_test_split(X, y, test_size=0.25)

boost = Boosting(n_estimators=3)
boost.fit(X_train, y_train, X_test, y_test)
boost.predict(X_train)