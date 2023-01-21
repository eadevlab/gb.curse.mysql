"""
Декоратор @classmethod
@classmethod — это метод, который получает класс в качестве неявного первого аргумента,
точно так же, как обычный метод экземпляра получает экземпляр.
Это означает, что вы можете использовать класс и его свойства внутри этого метода,
а не конкретного экземпляра.
"""

class TestClass(object):
    """
    Тестовый класс длы описания работы декоратора @classmethod
    """
    attribute_1 = 1 # Глобальный аттрибут класса
    attribute_2 = 1 # Глобальный аттрибут класса
    attribute_3 = 4 # Глобальный аттрибут класса

    def __init__(self, attribute_1: int, attribute_2:int):
        """
        Конструктор класса
        :param attribute_1: Какой-то аттрибут
        :param attribute_2: Какой-то аттрибут
        """
        self.attribute_1 = attribute_1
        self.attribute_2 = attribute_2
    @classmethod
    def get_attribute(cls):
        """
        Метод для возвращения аттрибута
        :return: int
        """
        return cls.attribute_1

    @classmethod
    def get_attribute_3(cls):
        """
        Метод для возвращения аттрибута
        :return: int
        """
        return cls.attribute_3

    def get_attribute_2(self):
        return self.attribute_2


testObject = TestClass(5,10) # Создание экземпляра класса с параметрами 1 и 10
print(testObject.get_attribute()) # Вернет 1
print(testObject.get_attribute_2()) # Вернет 10
"""
Почему так произошло?
При вызове get_attribute первый параметр cls, т.е. сам класс TestClass,
в котором глобально определен attribute_1 = 1
"""

"""
Попробуем получить аттрибут 2
"""
try:
    print(TestClass.get_attribute_2())
except TypeError:
    print('Ошибка получения аттрибута')
"""
Ошибка возникла потому что метод get_attribute_2 является методом объекта класса,
и обращается к self, которого у самого класса нет
Но можно передать этот самый объект)
"""
print(TestClass.get_attribute_2(testObject)) # Вернет 10

"""
Итого, classmethod хорошо использовать, когда необходимо получить методы,
не относящиеся к конкретному экземпляру класса, но все таки, как то привязанные к этому классу.
Эти методы можно переопределять дочерними классами.
Следовательно декоратор @classmethod уместно использовать в абстрактных классах для определения того,
как метод должен себя вести, когда он вызывается дочерними классами.
"""
print(TestClass.get_attribute()) # Вернет 1

# Выведем текущее значение аттрибута
print(TestClass.get_attribute_3()) # Вернет 4
print(testObject.get_attribute_3()) # Вернет 4
# Присвоим глобальному аттрибуту новое значение
TestClass.attribute_3 = 8
print(TestClass.get_attribute_3()) # Вернет 8
print(testObject.get_attribute_3()) # Вернет 8
# Присвоим аттрибуту объекта класса новое значение
testObject.attribute_3 = 50
# Попробуем получить через метов. Все они вернут значение аттрибута TestClass
print(TestClass.get_attribute_3()) # Вернет 8
print(testObject.get_attribute_3()) # Вернет 8
# А если обратится напрямую к аттрибуту
print(TestClass.attribute_3) # Вернет 8
print(testObject.attribute_3) # Вернет 50
