import moderngl
import random
from src.render.geom import Vertex
from units.unit_base import *  # должно быть в каждом юните
import numpy as nmp
import pygame  # временное решение

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
        w = h = 50
        self.w = w
        self.h = h

        self.g = self.rnd.geom(type='sphere', w=w, h=h)
        self.shd = self.rnd.shader('cloth', pattern='tex_c')
        self.grid = self.rnd.prim(self.g, shader=self.shd,
                    material= self.rnd.material('cloth mtl', ka=Vec3(.1, .1, .1), kd=Vec3(0.95, 0.95, 0.95),
                                            ks=Vec3(0.6, 0.6, 0.6), ph = 100))
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

            self.ubo[4 * i] = self.data[i].x
            self.ubo[4 * i + 1] = self.data[i].y
            self.ubo[4 * i + 2] = self.data[i].z


    def render(self):
        """
         Отрисовка будущей ткани.
         Аргументы: нет.
         Выходные данные: нет.
         """
        self.grid.render()

cloth_unit = ClothUnit()

