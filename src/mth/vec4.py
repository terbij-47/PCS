import random as random


class Vec4:

    @staticmethod
    def rnd() -> 'Vec4':
        """
        Создание вектора с произвольными компонентами в пределах [0, 1).
        Аргументы: нет.
        Выходные данные:
            (Vec4) произвольный вектор.
        """
        return Vec4(random.random(), random.random(), random.random(), random.random())

    @staticmethod
    def dist(v1, v2) -> float:
        """
        Нахождение расстояния между точками.
        Аргументы:
            - радиус-вектора точек:
                (Vec4) v1, v2
        Выходные данные:
            (float) расстояние между точками.
        """
        return (v1 - v2).len()

    def __init__( self, x : float = 0, y : float = 0, z : float = 0, w : float = 0 ) -> None:
        """
        Создание четырехкомпонентного вектора.
        Аргументы:
            - компоненты вектора:
                (float) x, y, z, w;
        """
        self.x = x
        self.y = y
        self.z = z
        self.w = w

    def len( self ) -> float:
        """
        Получение длины вектора.
        Аргументы: нет.
        Выходные данные:
            (float) длина вектора.
        """
        return (self.x ** 2 + self.y ** 2 + self.z ** 2 + self.w ** 2) ** 0.5

    def __add__(self, other : 'Vec4') -> 'Vec4':
        """
        Сложение двух векторов.
        Аргументы:
            - второй вектор:
                (Vec4) other;
        Выходные данные:
            (Vec4) результат сложения.
        """
        return Vec4(self.x + other.x,
                    self.y + other.y,
                    self.z + other.z,
                    self.w + other.w)

    def __sub__(self, other : 'Vec4') -> 'Vec4':
        """
        Вычитание двух векторов.
        Аргументы:
            - второй вектор:
                (Vec4) other;
        Выходные данные:
            (Vec4) результат вычитания.
        """
        return Vec4(self.x - other.x,
                    self.y - other.y,
                    self.z - other.z,
                    self.w - other.w)

    def __mul__(self, other):
        """
        Умножение вектора на объект.
        Аргументы:
            - второй вектор: (Vec4) other;
              число: (float) other;
        Выходные данные:
            (float) результат скалярного умножения векторов.
            (Vec4) результат умножения вектора на число.
        """

        if type(other) == float or type(other) == int:
            return Vec4(self.x * other, self.y * other, self.z * other, self.w * other)
        if type(other) == Vec4:
            return self.x * other.x + self.y * other.y + self.z * other.z + self.w * other.w
        raise TypeError(f'Cannot multiply 4d vector with {type(other)}')


    def __invert__(self) -> 'Vec4':
        """
        Получение нормированного вектора. Сам вектор не изменяется
        Аргументы: нет.
        Выходные данные:
            (Vec4) нормированный вектор.
        """
        l = self.len()
        if l == 0:
            return self
        return self / l

    def norm_self(self) -> 'Vec4':
        """
        Нормирование вектора. Изменяет данный вектор
        Аргументы: нет.
        Выходные данные:
            (Vec4) нормированный вектор.
        """
        l = self.len()
        if l == 0:
            return self
        self.x /= l
        self.y /= l
        self.z /= l
        self.w /= l
        return self

    def __truediv__(self, other : float) -> 'Vec4':
        """
        Деление вектора на число.
        Аргументы:
            - число:
                (float) other;
        Выходные данные:
            (Vec4) результат деления.
        """
        return Vec4(self.x / other, self.y / other, self.z / other, self.w / other)

    def __neg__(self) -> 'Vec4':
        """
        Умножение вектора на -1. Сам вектор не меняется
        Аргументы: нет.
        Выходные данные:
            (Vec4) развернутый вектор.
        """
        return Vec4(-self.x, -self.y, -self.z, -self.w)

    def __iadd__(self, other : 'Vec4') -> 'Vec4':
        """
        Прибавление вектора к данному.
        Аргументы:
            - второй вектор:
                (Vec4) other;
        Выходные данные:
            (Vec4) результирующий вектор.
        """
        self.x += other.x
        self.y += other.y
        self.z += other.z
        self.w += other.w
        return self

    def __isub__(self, other : 'Vec4') -> 'Vec4':
        """
        Вычитание вектора из текущего.
        Аргументы:
            - второй вектор:
                (Vec4) other;
        Выходные данные:
            (Vec4) результирующий вектор.
        """
        self.x -= other.x
        self.y -= other.y
        self.z -= other.z
        self.w -= other.w
        return self

    def __itruediv__(self, other = float) -> 'Vec4':
        """
        Деление вектора на число.
        Аргументы:
            - число:
                (float) other;
        Выходные данные:
            (Vec4) результирующий вектор.
        """
        self.x /= other
        self.y /= other
        self.z /= other
        self.w /= other
        return self

    def __imul__(self, other = float) -> 'Vec4':
        """
        Умножение вектора на число.
        Аргументы:
            - число:
                (float) other;
        Выходные данные:
            (Vec4) результирующий вектор.
        """
        self.x *= other
        self.y *= other
        self.z *= other
        self.w *= other
        return self

    def __str__(self) -> str:
        """
        Строковое представление вектора.
        Аргументы: нет.
        Выходные данные:
             (str) строка, содержащая компоненты вектора.
       """
        return f'x: {self.x}, y: {self.y}, z: {self.z}, w: {self.w}'

    def to_list(self) -> list:
        """
        Запись компонент вектора в виде списка.
        Аргументы: нет.
        Выходные данные:
            (list) список, состоящий из компонент вектора.
        """
        return [self.x, self.y, self.z, self.w]

    def to_tuple(self) -> tuple:
        """
        Запись компонент вектора в виде кортежа.
        Аргументы: нет.
        Выходные данные:
            (tuple) кортеж, состоящий из компонент вектора.
        """
        return self.x, self.y, self.z, self.w

    def copy(self) -> 'Vec4':
        """
        Копирование вектора.
        Аргументы: нет.
        Выходные данные:
            (Vec4) новый вектор, но с теми же координатами.
        """
        return Vec4(self.x, self.y, self.z, self.w)
