from src.mth.vec3 import Vec3
from src.mth.mth import D2R, math

class Matr4:
    """
    Внимание! Здесь используется нотация вектор-строка.
    Это значит, что вектор умножается на матрицу. Не наоборот.
    """

    @staticmethod
    def matr_determ_3x3( a00 : float, a01 : float, a02 : float,
                            a10 : float, a11 : float, a12 : float,
                            a20 : float, a21 : float, a22 : float) -> float:
        """
        Вычисление определителя матрицы 3х3.
        Аргументы:
            - компоненты матрицы:
                (float) a00, a01, a02, a10, a11, a12, a20, a21, a22
        Выходные данные:
            (float) определитель матрицы
        """
        return a00 * a11 * a22 + a01 * a12 * a20 + a02 * a10 * a21 - \
               a00 * a12 * a21 - a01 * a10 * a22 - a02 * a11 * a20

    @staticmethod
    def rotate(angle_in_degrees : float, vector : Vec3) -> 'Matr4':
        """
        Матрица поворота вокруг оси на заданный угол против часовой стрелки.
        Аргументы:
            - угол поворота в градусах:
                (float) angle_in_degrees;
            - вектор, определяющий ось:
                (Vec3) vector;
        Выходные данные:
            (Matr4) матрица поворота
        """
        v = ~vector
        angle = D2R(angle_in_degrees)

        s = math.sin(angle)
        c = math.cos(angle)

        return Matr4(
          v.x * v.x * (1 - c) + c,         v.x * v.y * (1 - c) + v.z * s,   v.x * v.z * (1 - c) - v.y * s,   0,
                v.y * v.x * (1 - c) - v.z * s,   v.y * v.y * (1 - c) + c,         v.y * v.z * (1 - c) + v.x * s,   0,
                v.z * v.x * (1 - c) + v.y * s,   v.z * v.y * (1 - c) - v.x * s,   v.z * v.z * (1 - c) + c,         0,
                0,                               0,                               0,                               1)


    @staticmethod
    def rotateX(angle_in_degree : float) -> 'Matr4':
        """
        Матрица поворота вокруг оси ОХ на заданный угол против часовой стрелки.
        Аргументы:
            - угол поворота в градусах:
                (float) angle_in_degrees;
        Выходные данные:
            (Matr4) матрица поворота
        """
        a = D2R(angle_in_degree)
        s = math.sin(a)
        c = math.cos(a)

        return Matr4(1,  0, 0, 0,
                           0,  c, s, 0,
                           0, -s, c, 0,
                           0,  0, 0, 1)

    @staticmethod
    def rotateY(angle_in_degree : float) -> 'Matr4':
        """
        Матрица поворота вокруг оси OY на заданный угол против часовой стрелки.
        Аргументы:
            - угол поворота в градусах:
                (float) angle_in_degrees;
        Выходные данные:
            (Matr4) матрица поворота
        """
        a = D2R(angle_in_degree)
        s = math.sin(a)
        c = math.cos(a)

        return Matr4(c, 0, -s, 0,
                           0, 1,  0, 0,
                           s, 0,  c, 0,
                           0, 0,  0, 1)


    @staticmethod
    def rotateZ(angle_in_degree : float) -> 'Matr4':
        """
        Матрица поворота вокруг оси OZ на заданный угол против часовой стрелки.
        Аргументы:
            - угол поворота в градусах:
                (float) angle_in_degrees;
        Выходные данные:
            (Matr4) матрица поворота
        """
        a = D2R(angle_in_degree)
        s = math.sin(a)
        c = math.cos(a)

        return Matr4( c, s, 0, 0,
                           -s, c, 0, 0,
                            0, 0, 1, 0,
                            0, 0, 0, 1)

    @staticmethod
    def scale(v : Vec3) -> 'Matr4':
        """
        Матрица масштабирования.
        Аргументы:
            - вектор, компоненты которого задают масштабные коэффициенты по соответствующим осям:
                (Vec3) v;
        Выходные данные:
            (Matr4) матрица масштабирования
        """
        return Matr4(v.x,   0,   0, 0,
                             0, v.y,   0, 0,
                             0,   0, v.z, 0,
                             0,   0,   0, 1)

    @staticmethod
    def translate(v : Vec3) -> 'Matr4':
        """
        Матрица параллельного переноса.
        Аргументы:
            - вектор, задающий смещение:
                (Vec3) v;
        Выходные данные:
            (Matr4) матрица параллельного переноса
        """
        return Matr4(1,   0,   0, 0,
                           0,   1,   0, 0,
                           0,   0,   1, 0,
                         v.x, v.y, v.z, 1)

    @staticmethod
    def ortho(left : float, right : float, bottom : float, top : float, near : float, far : float) -> 'Matr4':
        """
        Матрица ортогональной проекции.
        Аргументы:
            - горизонтальные границы видимости:
                (float) left, right;
            - вертикальные границы видимости:
                (float) bottom, top;
            - дальность видимости:
                (float) near, far;
        Выходные данные:
            (Matr4) матрица ортогональной проекции
        """
        return Matr4(
          2 / (right - left),                0,                                 0,                            0,
                0,                                 2 / (top - bottom),                0,                            0,
                0,                                 0,                                 -2 / (far - near),            0,
                -(right + left) / (right - left),  -(top + bottom) / (top - bottom),  -(far + near) / (far - near), 1)

    @staticmethod
    def frustum(left : float, right : float, bottom : float, top : float, near : float, far : float) -> 'Matr4':
        """
        Матрица центральной проекции.
        Аргументы:
            - границы видимости по горизонтали:
                (float) left, right;
            - границы видимости по вертикали:
                (float) bottom, top;
            - дальность видимости:
                (float) near, far;
        Выходные данные:
            (Matr4) матрица центральной проекции
        """
        l = left
        r = right
        b = bottom
        t = top
        n = near
        f = far
        return Matr4(
          2 * n / (r - l),   0,                 0,                    0,
                0,                 2 * n / (t - b),   0,                    0,
                (r + l) / (r - l), (t + b) / (t - b), -(f + n) / (f - n),  -1,
                0,                 0,                 -2 * n * f / (f - n), 0)

    @staticmethod
    def view(loc : Vec3, at : Vec3, up : Vec3) -> 'Matr4':
        """
        Матрица, которая задает обзор (не знаю, как иначе это написать).
        Аргументы:
            - радиус-вектор точки обзора:
                (Vec3) loc;
            - радиус-вектор точки, в которую смотрим:
                (Vec3) at;
            - вектор направления "наверх" в системе координат смотрящего:
                (Vec3) up;
        Выходные данные:
            (Matr4) матрица обзора
        """
        dir_ = ~(at - loc)
        right = ~(dir_ % up)
        tup = ~(right % dir_)
        return Matr4(
            right.x,        tup.x,        -dir_.x,      0,
                  right.y,        tup.y,        -dir_.y,      0,
                  right.z,        tup.z,        -dir_.z,      0,
                  -(loc * right), -(loc * tup), (loc * dir_), 1)

    def __init__(self, *args) -> None:
        """
        Создание матрицы 4х4.
        Аргументы:
            - нет.
            - список из 16 компонент матрицы: (list) *args;
        Выходные данные: нет
        """
        if len(args) == 0:
            self.A = [
                [1, 0, 0, 0],
                [0, 1, 0, 0],
                [0, 0, 1, 0],
                [0, 0, 0, 1]
            ]
        else:
            self.A = [
                [args[0], args[1], args[2], args[3]],
                [args[4], args[5], args[6], args[7]],
                [args[8], args[9], args[10], args[11]],
                [args[12], args[13], args[14], args[15]]
            ]
        self.__inv = None

    def __mul__(self, other : 'Matr4') -> 'Matr4':
        """
        Умножение матриц.
        Аргументы:
            - вторая матрица:
                (Matr4) other;
        Выходные данные:
            (Matr4) результат умножения.
        """
        if type(other) == Matr4:
            res = Matr4(0, 0, 0, 0,
                        0, 0, 0, 0,
                        0, 0, 0, 0,
                        0, 0, 0, 0)
            for i in range(4):
                for j in range(4):
                    for k in range(4):
                        res.A[i][j] += self.A[i][k] * other.A[k][j]
            return res

    def __invert__(self) -> float:
        """
        Определитель матрицы.
        Аргументы: нет.
        Выходные данные:
            (float) определитель матрицы.
        """
        return  \
           self.A[0][0] * Matr4.matr_determ_3x3(self.A[1][1], self.A[1][2], self.A[1][3],
                                                self.A[2][1], self.A[2][2], self.A[2][3],
                                                self.A[3][1], self.A[3][2], self.A[3][3]) \
                \
          -self.A[0][1] * Matr4.matr_determ_3x3(self.A[1][0], self.A[1][2], self.A[1][3],
                                                self.A[2][0], self.A[2][2], self.A[2][3],
                                                self.A[3][0], self.A[3][2], self.A[3][3]) \
                \
          +self.A[0][2] * Matr4.matr_determ_3x3(self.A[1][0], self.A[1][1], self.A[1][3],
                                                self.A[2][0], self.A[2][1], self.A[2][3],
                                                self.A[3][0], self.A[3][1], self.A[3][3]) \
                \
          -self.A[0][3] * Matr4.matr_determ_3x3(self.A[1][0], self.A[1][1], self.A[1][2],
                                                self.A[2][0], self.A[2][1], self.A[2][2],
                                                self.A[3][0], self.A[3][1], self.A[3][2])

    def inverse(self) -> 'Matr4':
        """
        Нахождение обратной матрицы.
        Аргументы: нет.
        Выходные данные:
            (Matr4) обратная матрица.
        """
        if self.__inv:
            return Matr4(*self.__inv)

        det = ~self

        r = Matr4()
        if det == 0:
            return r

        r.A[0][0] = \
          +Matr4.matr_determ_3x3(self.A[1][1], self.A[1][2], self.A[1][3],
                                 self.A[2][1], self.A[2][2], self.A[2][3],
                                 self.A[3][1], self.A[3][2], self.A[3][3]) / det
        r.A[1][0] = \
          -Matr4.matr_determ_3x3(self.A[1][0], self.A[1][2], self.A[1][3],
                                 self.A[2][0], self.A[2][2], self.A[2][3],
                                 self.A[3][0], self.A[3][2], self.A[3][3]) / det
        r.A[2][0] = \
          +Matr4.matr_determ_3x3(self.A[1][0], self.A[1][1], self.A[1][3],
                                 self.A[2][0], self.A[2][1], self.A[2][3],
                                 self.A[3][0], self.A[3][1], self.A[3][3]) / det
        r.A[3][0] = \
          -Matr4.matr_determ_3x3(self.A[1][0], self.A[1][1], self.A[1][2],
                                 self.A[2][0], self.A[2][1], self.A[2][2],
                                 self.A[3][0], self.A[3][1], self.A[3][2]) / det

        r.A[0][1] = \
          -Matr4.matr_determ_3x3(self.A[0][1], self.A[0][2], self.A[0][3],
                                 self.A[2][1], self.A[2][2], self.A[2][3],
                                 self.A[3][1], self.A[3][2], self.A[3][3]) / det
        r.A[1][1] = \
          +Matr4.matr_determ_3x3(self.A[0][0], self.A[0][2], self.A[0][3],
                                 self.A[2][0], self.A[2][2], self.A[2][3],
                                 self.A[3][0], self.A[3][2], self.A[3][3]) / det
        r.A[2][1] = \
          -Matr4.matr_determ_3x3(self.A[0][0], self.A[0][1], self.A[0][3],
                                 self.A[2][0], self.A[2][1], self.A[2][3],
                                 self.A[3][0], self.A[3][1], self.A[3][3]) / det
        r.A[3][1] = \
          +Matr4.matr_determ_3x3(self.A[0][0], self.A[0][1], self.A[0][2],
                                 self.A[2][0], self.A[2][1], self.A[2][2],
                                 self.A[3][0], self.A[3][1], self.A[3][2]) / det

        r.A[0][2] = \
          +Matr4.matr_determ_3x3(self.A[0][1], self.A[0][2], self.A[0][3],
                                 self.A[1][1], self.A[1][2], self.A[1][3],
                                 self.A[3][1], self.A[3][2], self.A[3][3]) / det
        r.A[1][2] = \
          -Matr4.matr_determ_3x3(self.A[0][0], self.A[0][2], self.A[0][3],
                                 self.A[1][0], self.A[1][2], self.A[1][3],
                                 self.A[3][0], self.A[3][2], self.A[3][3]) / det
        r.A[2][2] = \
          +Matr4.matr_determ_3x3(self.A[0][0], self.A[0][1], self.A[0][3],
                                 self.A[1][0], self.A[1][1], self.A[1][3],
                                 self.A[3][0], self.A[3][1], self.A[3][3]) / det
        r.A[3][2] = \
          -Matr4.matr_determ_3x3(self.A[0][0], self.A[0][1], self.A[0][2],
                                 self.A[1][0], self.A[1][1], self.A[1][2],
                                 self.A[3][0], self.A[3][1], self.A[3][2]) / det

        r.A[0][3] = \
          -Matr4.matr_determ_3x3(self.A[0][1], self.A[0][2], self.A[0][3],
                                 self.A[1][1], self.A[1][2], self.A[1][3],
                                 self.A[2][1], self.A[2][2], self.A[2][3]) / det
        r.A[1][3] = \
          +Matr4.matr_determ_3x3(self.A[0][0], self.A[0][2], self.A[0][3],
                                 self.A[1][0], self.A[1][2], self.A[1][3],
                                 self.A[2][0], self.A[2][2], self.A[2][3]) / det
        r.A[2][3] = \
          -Matr4.matr_determ_3x3(self.A[0][0], self.A[0][1], self.A[0][3],
                                 self.A[1][0], self.A[1][1], self.A[1][3],
                                 self.A[2][0], self.A[2][1], self.A[2][3]) / det
        r.A[3][3] = \
          +Matr4.matr_determ_3x3(self.A[0][0], self.A[0][1], self.A[0][2],
                                 self.A[1][0], self.A[1][1], self.A[1][2],
                                 self.A[2][0], self.A[2][1], self.A[2][2]) / det
        self.__inv = r.to_list()
        return r


    def transpose(self) -> 'Matr4':
        """
        Транспонирование матрицы
        Аргументы: нет.
        Выходные данные:
            (Matr4) транспонированная матрица
        """
        return Matr4(self.A[0][0], self.A[1][0], self.A[2][0], self.A[3][0],
                           self.A[0][1], self.A[1][1], self.A[2][1], self.A[3][1],
                           self.A[0][2], self.A[1][2], self.A[2][2], self.A[3][2],
                           self.A[0][3], self.A[1][3], self.A[2][3], self.A[3][3])

    def transform_hc(self, v : Vec3) -> Vec3:
        """
        Умножение вектора на матрицу с приведением вектора к гомогенным координатам
        Аргументы:
            - трехкомпонентный вектор:
                (Vec3) v;
        Выходные данные:
            (Vec3) преобразованный вектор с гомогенными координатами.
        """
        w = v.x * self.A[0][3] + v.y * self.A[1][3] + v.z * self.A[2][3] + self.A[3][3]

        return Vec3((v.x * self.A[0][0] + v.y * self.A[1][0] + v.z * self.A[2][0] + self.A[3][0]) / w,
                    (v.x * self.A[0][1] + v.y * self.A[1][1] + v.z * self.A[2][1] + self.A[3][1]) / w,
                    (v.x * self.A[0][2] + v.y * self.A[1][2] + v.z * self.A[2][2] + self.A[3][2]) / w)


    def transform_normal(self, v : Vec3) -> Vec3:
        """
        Преобразование вектора нормали. (точки объекта меняются по прямой матрице, а нормали - по обратной)
        Аргументы:
            - вектор нормали:
                (Vec3) v;
        Выходные данные:
            (Vec3) преобразованный вектор нормали.
        """
        t = self.inverse()
        return Vec3(v.x * t.A[0][0] + v.y * t.A[0][1] + v.z * t.A[0][2],
                    v.x * t.A[1][0] + v.y * t.A[1][1] + v.z * t.A[1][2],
                    v.x * t.A[2][0] + v.y * t.A[2][1] + v.z * t.A[2][2])

    def to_tuple(self) -> tuple:
        """
        Запись компонент матрицы в виде кортежа.
        Аргументы: нет.
        Выходные данные:
            (tuple) кортеж, состоящий из компонент матрицы.
        """
        return self.A[0][0], self.A[0][1], self.A[0][2], self.A[0][3], \
               self.A[1][0], self.A[1][1], self.A[1][2], self.A[1][3], \
               self.A[2][0], self.A[2][1], self.A[2][2], self.A[2][3], \
               self.A[3][0], self.A[3][1], self.A[3][2], self.A[3][3]

    def to_list(self) -> list:
        """
        Запись компонент матрицы в виде списка.
        Аргументы: нет.
        Выходные данные:
            (list) список, состоящий из компонент матрицы.
        """
        return [self.A[0][0], self.A[0][1], self.A[0][2], self.A[0][3],
                self.A[1][0], self.A[1][1], self.A[1][2], self.A[1][3],
                self.A[2][0], self.A[2][1], self.A[2][2], self.A[2][3],
                self.A[3][0], self.A[3][1], self.A[3][2], self.A[3][3]]

    def copy(self) -> 'Matr4':
        """
        Копирование матрицы.
        Аргументы: нет.
        Выходные данные:
            (Matr4) новая матрица, но с теми же компонентами.
        """
        return Matr4(self.A[0][0], self.A[0][1], self.A[0][2], self.A[0][3],
                self.A[1][0], self.A[1][1], self.A[1][2], self.A[1][3],
                self.A[2][0], self.A[2][1], self.A[2][2], self.A[2][3],
                self.A[3][0], self.A[3][1], self.A[3][2], self.A[3][3])