from src.mth.matr4 import Matr4, Vec3

class Camera:
    def __init__(self, loc = Vec3(0, 0, 10), up = Vec3(0, 1, 0), right = Vec3(1, 0, 0),
                 dir_ = Vec3(0, 0, 1), frame_w = 0, frame_h = 0):
        """
        Создание камеры.
        Аргументы:
            - радиус-вектор позиции камеры в мировой системе координат:
                (Vec3) loc;
            - вектор направления "наверх" относительно камеры:
                (Vec3) up;
            - вектор направления "направо" относительно камеры:
                (Vec3) right;
            - вектор направления, к котором смотрит камера:
                (Vec3) dir_
            - ширина кадра в пикселях:
                (int) frame_w;
            - высота кадра в пикселях:
                (int) frame_h;
        """
        self.loc = loc
        self.up = ~up
        self.right = ~right
        self.dir = ~dir_
        self.at = Vec3(0, 0, 5)

        self.frame_w = frame_w
        self.frame_h = frame_h
        self.proj_size = 0.2
        self.near = 0.1
        self.far = 16384

        self.proj = Matr4()
        self.view = Matr4()
        self.view_proj = Matr4()

    def proj_set(self):
        """
        Пересчет матрицы центральной проекции по заранее установленным размерам окна.
        Аргументы: нет.
        Выходные данные: нет.
        """
        rx = self.proj_size * self.frame_w / self.frame_h
        ry = self.proj_size

        self.proj = Matr4.frustum(-rx / 2, rx / 2, -ry / 2, ry / 2, self.near, self.far)
        self.view_proj = self.view * self.proj

    def reshape(self, frame_w, frame_h):
        """
        Пересчет матрицы центральной проекции по размерам окна.
        Аргументы:
            - ширина и высота кадра в пикселях:
                (int) frame_w, frame_h;
        Выходные данные: нет.
        """
        self.frame_h = frame_h
        self.frame_w = frame_w
        self.proj_set()

    def proj_set_ortho(self):
        """
        Пересчет матрицы ортогональной проекции по заранее установленным размерам окна.
        Аргументы: нет.
        Выходные данные: нет.
        """
        rx = self.proj_size * self.frame_w / self.frame_h
        ry = self.proj_size

        self.proj = Matr4.ortho(-rx / 2, rx / 2, -ry / 2, ry / 2, self.near, self.far)
        self.view_proj = self.view * self.proj

    def set(self, loc, at, up = Vec3(0, 1, 0)):
        """
        Установка камеры.
        Аргументы:
            - позиция камеры:
                (Vec3) loc;
            - точка, в которую смотрит камера:
                (Vec3) at;
            - направление "наверх" относительно камеры:
                (Vec3) up;
        Выходные данные: нет.
        """
        self.view = Matr4.view(loc, at, up)
        self.right = Vec3(self.view.A[0][0],
                          self.view.A[1][0],
                          self.view.A[2][0])
        self.up = Vec3(self.view.A[0][1],
                       self.view.A[1][1],
                       self.view.A[2][1])
        self.dir = Vec3(-self.view.A[0][2],
                        -self.view.A[1][2],
                        -self.view.A[2][2])
        self.loc = loc
        self.at = at
        self.view_proj = self.view * self.proj
