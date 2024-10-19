import random as random


class Vec3:

    @classmethod
    def rnd(cls):
        """
        Создание вектора с произвольными компонентами в пределах [0, 1).
        Аргументы: нет.
        Выходные данные:
            (Vec3) произвольный вектор.
        """
        return Vec3(random.random(), random.random(), random.random())

    @classmethod
    def dist(cls, v1, v2) -> float:
        """
        Нахождение расстояния между точками.
        Аргументы:
            - радиус-вектора точек:
                (Vec3) v1, v2
        Выходные данные:
            (float) расстояние между точками.
        """
        return (v1 - v2).len()

    def __init__( self, x : float = 0, y : float = 0, z : float = 0 ):
        """
        Создание трехкомпонентного вектора.
        Аргументы:
            - компоненты вектора:
                (float) x, y, z;
        """
        self.x = x
        self.y = y
        self.z = z

    def len( self ) -> float:
        """
        Получение длины вектора.
        Аргументы: нет.
        Выходные данные:
            (float) длина вектора.
        """
        return (self.x ** 2 + self.y ** 2 + self.z ** 2) ** 0.5

    def __add__(self, other):
        """
        Сложение двух векторов.
        Аргументы:
            - второй вектор:
                (Vec3) other;
        Выходные данные:
            (Vec3) результат сложения.
        """
        return Vec3(self.x + other.x,
                    self.y + other.y,
                    self.z + other.z)

    def __sub__(self, other):
        """
        Вычитание двух векторов.
        Аргументы:
            - второй вектор:
                (Vec3) other;
        Выходные данные:
            (Vec3) результат вычитания.
        """
        return Vec3(self.x - other.x,
                    self.y - other.y,
                    self.z - other.z)

    def __mul__(self, other):
        """
        Умножение вектора на объект.
        Аргументы:
            - второй вектор: (Vec3) other;
              число: (float) other;
              матрица: (Matr4) other;
        Выходные данные:
            (float) результат скалярного умножения векторов.
            (Vec3) результат умножения вектора на число.
            (Vec3) результат умножения соответствующего четырехкомпонентного вектора на матрицу.
                Используется нотация вектор-строка
        """

        if type(other) == float or type(other) == int:
            return Vec3(self.x * other, self.y * other, self.z * other)
        if type(other) == Vec3:
            return self.x * other.x + self.y * other.y + self.z * other.z
        if other.A:
            return Vec3(self.x * other.A[0][0] + self.y * other.A[1][0] + self.z * other.A[2][0] + other.A[3][0],
                        self.x * other.A[0][1] + self.y * other.A[1][1] + self.z * other.A[2][1] + other.A[3][1],
                        self.x * other.A[0][2] + self.y * other.A[1][2] + self.z * other.A[2][2] + other.A[3][2])
        return None

    def __and__(self, other):
        """
        Умножение вектора на матрицу 3х3.
        Аргументы:
            - матрица:
                (Matr4) other;
        Выходные данные:
            (Vec3) результат умножения трехкомпонентного вектора на соответствующую матрицу 3х3.
                Используется нотация вектор-строка
        """
        return Vec3(self.x * other.A[0][0] + self.y * other.A[1][0] + self.z * other.A[2][0],
                    self.x * other.A[0][1] + self.y * other.A[1][1] + self.z * other.A[2][1],
                    self.x * other.A[0][2] + self.y * other.A[1][2] + self.z * other.A[2][2])



    def __mod__(self, other):
        """
        Вычисление векторного произведения векторов.
        Аргументы:
            - второй вектор:
                (Vec3) other;
        Выходные данные:
            (Vec3) результат векторного произведения.
        """
        return Vec3(self.y * other.z - self.z * other.y,
                    self.z * other.x - self.x * other.z,
                    self.x * other.y - self.y * other.x)

    def __invert__(self):
        """
        Получение нормированного вектора. Сам вектор не изменяется
        Аргументы: нет.
        Выходные данные:
            (Vec3) нормированный вектор.
        """
        l = self.len()
        if l == 0:
            return self
        return self / l

    def norm_self(self):
        """
        Нормирование вектора. Изменяет данный вектор
        Аргументы: нет.
        Выходные данные:
            (Vec3) нормированный вектор.
        """
        l = self.len()
        if l == 0:
            return self
        self.x /= l
        self.y /= l
        self.z /= l
        return self

    def __truediv__(self, other : float):
        """
        Деление вектора на число.
        Аргументы:
            - число:
                (float) other;
        Выходные данные:
            (Vec3) результат деления.
        """
        return Vec3(self.x / other, self.y / other, self.z / other)

    def __neg__(self):
        """
        Умножение вектора на -1. Сам вектор не меняется
        Аргументы: нет.
        Выходные данные:
            (Vec3) развернутый вектор.
        """
        return Vec3(-self.x, -self.y, -self.z)

    def __iadd__(self, other):
        """
        Прибавление вектора к данному.
        Аргументы:
            - второй вектор:
                (Vec3) other;
        Выходные данные: нет.
        """
        self.x += other.x
        self.y += other.y
        self.z += other.z
        return self

    def __isub__(self, other):
        """
        Вычитание вектора из текущего.
        Аргументы:
            - второй вектор:
                (Vec3) other;
        Выходные данные: нет.
        """
        self.x -= other.x
        self.y -= other.y
        self.z -= other.z
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
        self.z /= other
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
        self.z *= other
        return self

    def to_list(self):
        """
        Запись компонент вектора в виде списка.
        Аргументы: нет.
        Выходные данные:
            (list) список, состоящий из компонент вектора.
        """
        return [self.x, self.y, self.z]

    def to_tuple(self):
        """
        Запись компонент вектора в виде кортежа.
        Аргументы: нет.
        Выходные данные:
            (tuple) кортеж, состоящий из компонент вектора.
        """
        return self.x, self.y, self.z
