import random as random

class Vec2:

    @classmethod
    def rnd(cls):
        """
        Создание вектора со случайными координатами в пределах [0, 1).
        Аргументы: нет.
        Выходные данные:
            (Vec2) произвольный вектор.
        """
        return Vec2(random.random(), random.random())


    def __init__(self, x : float = 0, y : float = 0):
        """
        Создание двухкомпонентного вектора.
        Аргументы:
            - координаты вектора:
                (float) x, y;
        """
        self.x = x
        self.y = y

    def len(self) -> float:
        """
        Нахождение длины вектора.
        Аргументы: нет.
        Выходные данные:
            (float) длина вектора
        """
        return (self.x ** 2 + self.y ** 2) ** 0.5

    def __add__(self, other):
        """
        Нахождение суммы векторов.
        Аргументы:
            - второй вектор:
                (Vec2) other;
        Выходные данные:
            (Vec2) сумма векторов
        """
        return Vec2(self.x + other.x,
                    self.y + other.y)

    def __sub__(self, other):
        """
        Нахождение разности векторов.
        Аргументы:
            - второй вектор:
                (Vec2) other;
        Выходные данные:
            (Vec2) разность векторов
        """
        return Vec2(self.x - other.x,
                    self.y - other.y)

    def __mul__(self, other):
        """
        Умножение вектора на другой математический объект.
        Аргументы:
            - второй вектор: (Vec2) other;
            - число: (float) other;
        Выходные данные:
            (float) скалярное произведение векторов.
            (Vec2) вектор, умноженный на заданное число.
        """
        if type(other) == float or type(other) == int:
            return Vec2(self.x * other, self.y * other)
        if type(other) == Vec2:
            return self.x * other.x + self.y * other.y
        return None


    def __invert__(self):
        """
        Нахождение нормированного вектора. Сам вектор не изменяется.
        Аргументы: нет.
        Выходные данные:
            (Vec2) нормированный вектор.
        """
        l = self.len()
        if l == 0:
            return self
        return self / l

    def norm_self(self):
        """
        Нормирование вектора.
        Аргументы: нет.
        Выходные данные:
            (Vec2) нормированный вектор.
        """
        l = self.len()
        if l == 0:
            return self
        self.x /= l
        self.y /= l
        return self

    def __truediv__(self, other):
        """
        Деление вектора на число.
        Аргументы:
            - число:
                (float) other;
        Выходные данные:
            (Vec2) итоговый вектор.
        """
        return Vec2(self.x / other, self.y / other)

    def __neg__(self):
        """
        Умножение вектора на -1. Сам вектор не меняется
        Аргументы: нет.
        Выходные данные:
            (Vec2) развернутый вектор.
        """
        return Vec2(-self.x, -self.y)

    def __iadd__(self, other):
        """
        Прибавление вектора к данному.
        Аргументы:
            - второй вектор:
                (Vec2) other;
        Выходные данные: нет.
        """
        self.x += other.x
        self.y += other.y
        return self

    def __isub__(self, other):
        """
        Вычитание вектора из текущего.
        Аргументы:
            - второй вектор:
                (Vec2) other;
        Выходные данные: нет.
        """
        self.x -= other.x
        self.y -= other.y
        return self

    def __itruediv__(self, other = float):
        """
        Деление вектора на число.
        Аргументы:
            - число:
                (float) other;
        Выходные данные: нет.
        """
        self.x /= other
        self.y /= other
        return self

    def __imul__(self, other = float):
        """
        Домножение вектора на число.
        Аргументы:
            - число:
                (float) other;
        Выходные данные: нет.
        """
        self.x *= other
        self.y *= other
        return self

    def to_list(self) -> list:
        """
        Запись компонент вектора в список.
        Аргументы: нет.
        Выходные данные:
            (list) список, состоящий из компонент вектора.
        """
        return [self.x, self.y]

    def to_tuple(self) -> tuple:
        """
        Запись компонент вектора в кортеж.
        Аргументы: нет.
        Выходные данные:
            (tuple) кортеж, состоящий из компонент вектора.
        """
        return self.x, self.y

    def copy(self):
        """
        Копирование вектора.
        Аргументы: нет.
        Выходные данные:
            (Vec2) новый вектор, но с теми же координатами.
        """
        return Vec2(self.x, self.y)

