"""
4. Начните работу над проектом «Склад оргтехники». Создайте класс, описывающий склад.
А также класс «Оргтехника», который будет базовым для классов-наследников.
Эти классы — конкретные типы оргтехники (принтер, сканер, ксерокс).
В базовом классе определить параметры, общие для приведенных типов.
В классах-наследниках реализовать параметры, уникальные для каждого типа оргтехники.

5. Продолжить работу над четвертым заданием.
Разработать методы, отвечающие за приём оргтехники на
склад и передачу в определенное подразделение компании.
Для хранения данных о наименовании и
количестве единиц оргтехники, а также других данных,
можно использовать любую подходящую структуру, например словарь.

6. Продолжить работу над пятым заданием. Р
еализуйте механизм валидации вводимых пользователем данных.
Например, для указания количества принтеров,
отправленных на склад, нельзя использовать строковый тип данных.
Подсказка: постарайтесь по возможности реализовать в проекте
«Склад оргтехники» максимум возможностей, изученных на уроках по ООП.
"""


class MyOwnExc(Exception):
    """
    Создание собственного исключения
    """
    def __init__(self, txt):
        self.txt = txt


class OfficeEquipment:
    """
    Базовый класс для оффисного оборудования
    """
    def __init__(self, name:str, price:int, quantity:int, number_of_lists: int):
        """
        Конструктор
        :param name: Название оборудования
        :param price: Цена
        :param quantity: Количество
        :param number_of_lists: Номер в списке
        """
        self.name = name
        self.price = price
        self.numb = number_of_lists
        try:
            if isinstance(quantity, int): # Если количество целое число можно сформировать словарь

                self.quantity = quantity
                # Создание словаря оборудовния
                self.my_unit = {
                    'Модель устройства': self.name,
                    'Цена за ед': self.price,
                    'Количество': self.quantity}
            else:
                self.my_unit = {}
                # Выброс исключения
                raise MyOwnExc("Вы ввели не число, словарь будем пустым")

        except MyOwnExc as e:
            """
            Обработка исключения.
            В данном случае просто выводится текстовое сообщение,
            но объект класса создаётся
            """
            print(e.txt)


class Warehouse:
    """
    Класс описывающий поведение склада
    """
    goods = [] # Оборудование на складе

    @classmethod
    def reception(cls, obj:OfficeEquipment):
        """
        Добавление оборудовния на склад
        :param obj: Оборудование OfficeEquipment
        :return:
        """
        cls.goods.append(obj.my_unit)

    @classmethod
    def put_to_div(cls, obj, div):
        pass


class Printer(OfficeEquipment):
    """
    Класс описывающий работу принтера.
    Дочерний класс OfficeEquipment
    Наследует все свойства OfficeEquipment
    """
    def to_print(self):
        return f'to print smth {self.numb} times'


class Scanner(OfficeEquipment):
    """
    Класс описывающий работу принтера.
    Дочерний класс OfficeEquipment
    Наследует все свойства OfficeEquipment
    """
    def to_scan(self):
        return f'to scan smth {self.numb} times'


class Copier(OfficeEquipment):
    """
    Класс описывающий работу принтера.
    Дочерний класс OfficeEquipment
    Наследует все свойства OfficeEquipment
    """
    def to_copier(self):
        return f'to copier smth  {self.numb} times'


"""
Основная часть программы которая выполняется при запуске скрипта
До этого участка всё лишь объявление классов, функций
"""
unit_1 = Printer('hp', 2000, 5, 10) # Создание объекта принтер
unit_2 = Scanner('Canon', 1200, 5, 10) # Создание объекта сканер
Warehouse.reception(unit_1) # Добавление объекта на склад
Warehouse.reception(unit_2) # Добавление объекта на склад

print(Warehouse.goods) # Добавление информации о товарах на складе
print(unit_2.to_scan()) # Вызов метода to_scan класса Scaner

"""
Стоит отдельно отметить Warehouse
т.к. все методы в нём являются методами класса и единственный аттрибут
глобальный на уровне класса, то все созданные объекты будут идентичными
"""

wh = Warehouse()
assert wh.goods == Warehouse.goods
wh2 = Warehouse()
wh2.reception(unit_1)
wh.reception(unit_2)
assert wh.goods == wh2.goods
assert Warehouse.goods == wh2.goods
"""
Но тут есть один не приятный момент, все новые экземпляры хоть и идентичны,
но ссылаются на разные отделы памяти, чтоб это не случалось можно
модернизировать класс под так называемый Singleton
"""
assert wh != wh2 # Ошибки нет, классы разные

class WarehouseSingleton(Warehouse):
    """
    Пример реализации singelton
    """
    def __new__(cls):
        """
        Создание экземпляра класса
        """
        if not hasattr(cls, 'instance'):
            """
            Если ещё не существует созданного экземпляра класса
            его необходимо создать и присвоить аттрибуту, обычно используют 
            название instance
            """
            cls.instance = super(WarehouseSingleton, cls).__new__(cls)
        return cls.instance

"""
И всё, теперь все созданные экземпляры класса WarehouseSingleton
будут ссслаться на один блок памяти.
Проверим
"""
wh1  = WarehouseSingleton()
wh2 = WarehouseSingleton()

assert wh1 == wh2 # Ошибки нет, всё ок
print(wh1)
print(wh2)