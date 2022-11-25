"""
Общие замечания:
У классов и методов отсутсвует документирование и аннотация аттрибутов
https://peps.python.org/pep-0008/#documentation-strings
https://habr.com/ru/post/499358/

Очень не хватает тестового сценария проверки работоспособности кода,
например, как было в задании

Информация для изучения:
https://github.com/zedr/clean-code-python?ysclid=latmku9gbm269701636#translation
https://peps.python.org/pep-0008/

"""

# Если планируете использовать только определённый класс библиотеки
# то имеет смысл импортировать только его, это улучшит читаемость кода
# пример: from datetime import datetime as dt
import datetime as dt


class Record:
    # Пример документирования класса
    # """ Класс записей для калькулятора. """
    def __init__(self, amount, comment, date=''):
        # Пример документирования метода и его аттрибутов
        """
        Конструктор класса Record

        Parameters:
        amount (float): Описание параметра
        comment (str): Описание параметра
        date (str): Описание параметра
        """
        self.amount = amount

        # Код нечитабелен, отформатирован не по PEP8
        # Более красивой и понятной будет использование конструкции if else
        # Или, если интересно можо использовать сеттеры и геттеры
        # См. https://pythonpip.ru/osnovy/gettery-settery-python
        self.date = (
            dt.datetime.now().date() if
            not
            date else dt.datetime.strptime(date, '%d.%m.%Y').date())
        self.comment = comment


class Calculator:
    def __init__(self, limit):
        self.limit = limit
        # Для удобства можно указать тип переменной
        # self.records: List[Record] = []
        self.records = []

    def add_record(self, record):
        self.records.append(record)

    def get_today_stats(self):
        today_stats = 0
        # Переменные именуются с маленькой буквы
        # Record уже используется для именования класса
        for Record in self.records:
            # нет смысла каждый раз получать текущую дату
            # её можно вынести в отдельную переменную
            if Record.date == dt.datetime.now().date():
                # Можно использовать упрощенный вариант
                # today_stats += Record.amount
                today_stats = today_stats + Record.amount
        return today_stats

    def get_week_stats(self):
        week_stats = 0
        today = dt.datetime.now().date()
        for record in self.records:
            # Данное выражение можно упростить
            # 0 <= (today - record.date).days < 7
            if (
                    (today - record.date).days < 7 and
                    (today - record.date).days >= 0
            ):
                week_stats += record.amount
        return week_stats


class CaloriesCalculator(Calculator):
    # Комментарий к методу должен быть docstring
    # См. https://peps.python.org/pep-0257/#one-line-docstrings
    def get_calories_remained(self):  # Получает остаток калорий на сегодня
        # Ошибка!
        # Переменным лучше давать осмысленные названия
        # В требованиях к заданию указывается
        # что не доджно быть однобуквенных названий
        x = self.limit - self.get_today_stats()
        if x > 0:
            return f'Сегодня можно съесть что-нибудь' \
                   f' ещё, но с общей калорийностью не более {x} кКал'
        # else лишний, т.к. если условие выше произошло то метод вернет ответ
        else:
            # Скобки лишние
            return ('Хватит есть!')


class CashCalculator(Calculator):
    USD_RATE = float(60)  # Курс доллар США.
    EURO_RATE = float(70)  # Курс Евро.

    def get_today_cash_remained(self, currency,
                                USD_RATE=USD_RATE, EURO_RATE=EURO_RATE):
        # Переменная лишняя, можно использовать currency
        currency_type = currency
        # Получение остатков лучше вынести в отдельным метод базового класса
        cash_remained = self.limit - self.get_today_stats()
        # При желании данный кусок кода можно упростить c помощью глобального
        # словаря валют
        if currency == 'usd':
            cash_remained /= USD_RATE
            currency_type = 'USD'
        elif currency_type == 'eur':
            cash_remained /= EURO_RATE
            currency_type = 'Euro'
        elif currency_type == 'rub':
            # Ошибка!
            # == - логическая операция сравнения
            # для присвоения используется =
            cash_remained == 1.00
            currency_type = 'руб'
        if cash_remained > 0:
            return (
                f'На сегодня осталось {round(cash_remained, 2)} '
                f'{currency_type}'
            )
        elif cash_remained == 0:
            return 'Денег нет, держись'
        # Вместо elif можно использовать else
        elif cash_remained < 0:
            # Ошибка! В требованиях к коду сказано:
            # "Бэкслеши для переносов не применяются"
            return 'Денег нет, держись:' \
                   ' твой долг - {0:.2f} {1}'.format(-cash_remained,
                                                     currency_type)

    # Бессмысленное переопределение родительского метода
    # Переопределять метод родительского класса необходимо если вы хотите
    # дополнить его или полностью переписать
    def get_week_stats(self):
        # Ошибка! Отсутсвует return
        # в результате чего вызов метода всегда будет возвращать None
        super().get_week_stats()


"""
Выводы:
В данном коде присутсвует две ошибки из за которых работать будет некорректно.
В остальном все замечания касаются документирования и оптимизации
В целом не плохо, 3 из 5
"""