import moderngl

from src.mth.vec3 import Vec3
from src.mth.vec2 import Vec2
from src.mth.vec4 import Vec4
import math

class Vertex:
    offset = {'pos': (0, 3), 'norm': (3, 6), 'tex_c': (6, 8), 'color': (8, 12)}

    def __init__(self, pos = Vec3(), norm = Vec3(), tex_coord = Vec2(), color = Vec4()) -> None:
        """
        Инициализация класса вертекса.
        Аргументы:
            - позиция точки:
                (Vec3) pos;
            - нормаль к поверхности в точке:
                (Vec3) norm;
            - текстурные координаты:
                (Vec2) tex_coord;
            - цвет точки:
                (Vec4) color;
        Выходные данные: нет.
        """
        self.pos = pos
        self.norm = norm
        self.tex_coord = tex_coord
        self.color = color

    def to_array(self) -> list[float]:
        """
        Запись всех компонент вертекса в список.
        Аргументы: нет.
        Выходные данные:
            (list[float]) список всех вертекса.
        """
        return [self.pos.x, self.pos.y, self.pos.z,
                self.norm.x, self.norm.y, self.norm.z,
                self.tex_coord.x, self.tex_coord.y,
                self.color.x, self.color.y, self.color.z, self.color.w]


class Geometry:

    def __init__(self) -> None:
        """
        Инициализация класса геометрии.
        Аргументы: нет.
        Выходные данные: нет.
        """
        self.vertex_array = []
        self.index_array = None
        self.geom_type = moderngl.TRIANGLE_STRIP
        self.transform = None
        self.vertex_count = 0

    def plane(self) -> 'Geometry':
        """
        Создание геометрии единичной плоскости в начале координат.
        Аргументы: нет.
        Выходные данные:
            (self) заполненная геометрия.
        """
        self.vertex_array = [Vertex(pos = Vec3(0, 0, 0), norm = Vec3(0, 1, 0), tex_coord = Vec2(0, 0)),
                             Vertex(pos = Vec3(0, 0, 1), norm = Vec3(0, 1, 0), tex_coord = Vec2(0, 1)),
                             Vertex(pos = Vec3(1, 0, 0), norm = Vec3(0, 1, 0), tex_coord = Vec2(1, 0)),
                             Vertex(pos = Vec3(1, 0, 1), norm = Vec3(0, 1, 0), tex_coord = Vec2(1, 1))]
        self.geom_type = moderngl.TRIANGLE_STRIP
        return self

    def grid(self, w : int = 10, h : int = 10) -> 'Geometry':
        """
        Создание геометрии сетки с заданным разбиением.
        Аргументы:
            - количество точек в ширину и в высоту:
                (int) w, h;
        Выходные данные:
            (self) заполненная геометрия.
        """
        self.vertex_array = [i for i in range(w * h)]
        self.index_array= []
        for z in range(h):
            for x in range(w):
                self.vertex_array[z * w + x] = Vertex(pos = Vec3(x - (w - 1) / 2, 0, z - (h - 1) / 2),
                                                      norm= Vec3(0, 1,0),
                                                      tex_coord=Vec2(x / (w - 1), z / (h - 1)))
                if z < h - 1:
                    self.index_array.append((z + 1) * w + x)
                    self.index_array.append(z * w + x)
            if z < h - 2:
                self.index_array.append(-1)
        self.geom_type = moderngl.TRIANGLE_STRIP
        return self

    def sphere(self, w : int = 10, h : int = 10) -> 'Geometry':
        """
        Создание геометрии сферы с единичным радиусом в начале координат с заданным разбиением.
        Аргументы:
            - разбиение по широте и долготе:
                (int) w, h;
        Выходные данные:
            (self) заполненная геометрия.
        """
        self.grid(w, h)
        theta, phi, k = 0, 0, 0
        for i in range(h):
            for j in range(w):
                self.vertex_array[k].pos = Vec3(math.sin(theta) * math.sin(phi), math.cos(theta), math.sin(theta) * math.cos(phi))
                self.vertex_array[k].norm = self.vertex_array[k].pos.copy()
                k += 1
                phi += 2 * math.pi / (w - 1)
            phi = 0
            theta += math.pi / (h - 1)
        return self
    
    def torus(self, r : float | int = 0.3, w : int = 20, h : int = 10) -> 'Geometry':
        """
        Создание геометрии тора с единичным внешним радиусом в начале координат с заданным разбиением.
        Аргументы:
            - внутренний радиус тора:
                (float) r;
            - разбиение по широте и долготе:
                (int) w, h;
        Выходные данные:
            (self) заполненная геометрия.
        """
        self.grid(h, w)
        theta, phi, k = 0, 0, 0
        for i in range(w):
            offset = Vec3(math.cos(theta), 0, math.sin(theta))
            for j in range(h):
                cos1 = math.cos(phi) * r + 1
                self.vertex_array[k].pos = Vec3(offset.x * cos1, math.sin(phi) * r, offset.z * cos1)
                self.vertex_array[k].norm = ~(self.vertex_array[k].pos - offset)
                k += 1
                phi += 2 * math.pi / (h - 1)
            phi = 0
            theta += 2 * math.pi / (w - 1)
        return self

    def box(self) -> 'Geometry':
        """
        Создание геометрии куба с единичными сторонами в начале координат.
        Аргументы: нет.
        Выходные данные:
            (self) заполненная геометрия.
        """
        self.index_array = []
        norms = [Vec3(0, -1, 0), Vec3(0, 1, 0), Vec3(0, 0, 1), Vec3(1, 0, 0), Vec3(0, 0, -1), Vec3(-1, 0,0)]
        tex = [Vec2(0, 0), Vec2(0, 1), Vec2(1, 0), Vec2(1, 1)]
        self.vertex_array = [
            Vertex(pos=Vec3(0, 0, 0)), Vertex(pos=Vec3(0, 0, 1)), Vertex(pos=Vec3(1, 0, 0)), Vertex(pos=Vec3(1, 0, 1)),
            Vertex(pos=Vec3(0, 1, 1)), Vertex(pos=Vec3(0, 1, 0)), Vertex(pos=Vec3(1, 1, 1)), Vertex(pos=Vec3(1, 1, 0)),
            Vertex(pos=Vec3(0, 0, 1)), Vertex(pos=Vec3(0, 1, 1)), Vertex(pos=Vec3(1, 0, 1)), Vertex(pos=Vec3(1, 1, 1)),
            Vertex(pos=Vec3(1, 0, 1)), Vertex(pos=Vec3(1, 1, 1)), Vertex(pos=Vec3(1, 0, 0)), Vertex(pos=Vec3(1, 1, 0)),
            Vertex(pos=Vec3(1, 0, 0)), Vertex(pos=Vec3(1, 1, 0)), Vertex(pos=Vec3(0, 0, 0)), Vertex(pos=Vec3(0, 1, 0)),
            Vertex(pos=Vec3(0, 0, 0)), Vertex(pos=Vec3(0, 1, 0)), Vertex(pos=Vec3(0, 0, 1)), Vertex(pos=Vec3(0, 1, 1)),
        ]
        for plane in range(6):
            for point in range(4):
                self.vertex_array[plane * 4 + point].norm = norms[plane]
                self.vertex_array[plane * 4 + point].tex_coord = tex[point]
                self.index_array.append(plane * 4 + point)
            self.index_array.append(-1)
        self.index_array.pop()
        self.geom_type = moderngl.TRIANGLE_STRIP
        return self



