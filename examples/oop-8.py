class Person:
    """
    Базовый класс
    """
    def __init__(self, name: str, surname: str):
        """
        Конструкто.
        :param name: str Имя
        :param surname: str Фамилия
        """
        self.name = name
        self.surname = surname

    def __str__(self) -> str:
        """
        Метод вывода информации о объекте
        :return: str
        """
        return f"Name and surname: {self.name} {self.surname}"

class Teacher(Person):
    """
    Класс учителя
    """
    def to_teach(self, subj, *pupils):
        """
        Взять на обучение
        :param subj: str Тема урока
        :param pupils: Pupil Ученики
        """
        for pupil in pupils:
            pupil.to_take(subj)

class Pupil(Person):
    """
    Класс ученика
    """

    def __init__(self, name, surname):
        """
        Переопределение конструктора класса People
        :param name: str Имя
        :param surname: str Фамилия
        """
        super().__init__(name, surname)
        self.knowledges = []

    def to_take(self, subj):
        """
        Добавление пройденного материала
        :param subj: str Тема урока
        """
        self.knowledges.append(subj)

class Subject:
    """
    Предметы
    """
    def __init__(self, *subjects):
        """
        Конструктор
        :param subjects:
        """
        self.subjects = list(subjects)

    def my_list(self):
        """
        Возврат списка предметов
        :return: list
        """
        return self.subjects


s = Subject("maths", "physics", "chemistry") # создание объекта предметов
t = Teacher("Ivan", "Ivanov") # создание объекта учителя
print(t) # вызовет метод __str__ класса Teacher(Person)
p_1 = Pupil("Petr", "Petrov") # Создание ученика 1
p_2 = Pupil("Sergey", "Sergeev") # Создание ученика 2
p_3 = Pupil("Vladimir", "Vladimirov") # Создание ученика 3
print(f"{p_1}; {p_2}; {p_3}") # Вывод информации о учениках, вызовет метод __str__
t.to_teach(s, p_1, p_2, p_3)
print(p_1.knowledges[0].my_list()) # Вывод информации о предметах студента