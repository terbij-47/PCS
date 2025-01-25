import random
from units.unit_base import *  # должно быть в каждом юните


class ClothUnit(UnitBase):
    """
    Предполагается юнит рисования ткани по заданным точкам.
    Пока что это просто юнит рисования заданных позиций.
    """
    def __init__(self, w = 100, h = 100):
        """
        Конструктор класса.
        Аргументы: нет.
        Выходные данные: нет.
        """
        super().__init__()
        w = h = 30
        self.w = w
        self.h = h

        self.cloth = self.phys.cloth(w, h)

        self.g = self.rnd.geom(type='sphere', w=w, h=h)

        self.lgh2 = self.rnd.light(dir=Vec3(1, 3, 1), color=Vec3(0, 0.2, 0.2))
        self.lgh2.is_active = True

        self.shd = self.rnd.shader('cloth', pattern='tex_c')
        self.grid = self.rnd.prim(self.g, shader=self.shd,
                    material= self.rnd.material('cloth mtl', ka=Vec3(.1, .1, .1), kd=Vec3(0.95, 0.95, 0.95),
                                            ks=Vec3(0.6, 0.6, 0.6), ph = 100, tex2=['wood.png']) )

        self.ubo = self.grid.create_ubo(1, 4 * w * h)

        self.data = [Vec3() for i in range(w * h)]

        for i in range(len(self.grid.geom.vertex_array)):
            p = self.grid.geom.vertex_array[i].pos
            self.grid.geom.vertex_array[i].pos = p * ( 0.6 + random.random() / 10)

        self.shd['w']= w
        self.shd['h'] = h

    def update(self):
        """
        Обновление UBO параметров ткани.
        Аргументы: нет.
        Выходные данные: нет.
        """
        for i in range(len(self.grid.geom.vertex_array)):
            p = self.grid.geom.vertex_array[i].pos
            self.data[i] = p * (1.5 + math.sin(p.len() * self.timer.time / 200) / 1)

        for x in range(self.w):
            for y in range(self.h):
                i = self.w * y + x
                self.data[i] = self.cloth.grid[x][y].pos * 100

                self.ubo[4 * i] = self.data[i].x
                self.ubo[4 * i + 1] = self.data[i].y
                self.ubo[4 * i + 2] = self.data[i].z

    def render(self):
        """
         Отрисовка будущей ткани.
         Аргументы: нет.
         Выходные данные: нет.
         """
        self.cloth.update(self.timer.delta_time)
        self.grid.render()


cloth_unit = ClothUnit()

