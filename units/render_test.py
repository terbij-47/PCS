from units.unit_base import *  # должно быть в каждом юните

class TestRenderUnit(UnitBase):
    """
    Тестовый юнит для проверки работы рендера.
    Наследование базового класса обязательно.
    """
    def __init__(self):
        """
        Конструктор класса.
        Аргументы: нет.
        Выходные данные: нет.
        """
        super().__init__()

        sphere_mtl = self.rnd.material(name='black plastic', ka=Vec3(0.1, 0.1, 0.1), kd=Vec3(0.64, 0.84, 0.84), ks=Vec3(1,1,1)/1.2, ph=15, tex2=['metal.png'])
        th_mtl = self.rnd.material()

        self.sphere_count = 15
        self.R1 = (5, 7, 10, 14, 19)
        self.r1 = [math.sin(math.pi / self.sphere_count) * self.R1[i] * 0.4 for i in range(len(self.R1))]

        sphere = self.rnd.prim(self.rnd.geom(type='sphere', w=40, h=20),
                                                    material=sphere_mtl, inst_c=self.sphere_count)
        for i in range(self.sphere_count):
            phi = i * math.pi / self.sphere_count
            sphere.transform[i] = Matr4.rotateX(90) * Matr4.scale(Vec3(self.r1[0], self.r1[0] / 1.5, self.r1[0])) * \
                                    Matr4.translate(Vec3(self.R1[0] * math.sin(phi), 0, self.R1[0] * math.cos(phi)))
        torus = self.rnd.prim(self.rnd.geom(type='torus', r=self.r1[0] * 0.2 / self.R1[0], w=40, h=20),
                                                   material=th_mtl, inst_c=2)
        torus.transform[0] = Matr4.scale(Vec3(1.12, 0.3, 1.12)) * Matr4.scale(Vec3(self.R1[0], self.R1[0], self.R1[0]))
        torus.transform[1] = Matr4.scale(Vec3(0.88, 0.3, 0.88)) * Matr4.scale(Vec3(self.R1[0], self.R1[0], self.R1[0]))
        torus.transform[0] = Matr4.scale(Vec3(.3, 0.7, .3)) * Matr4.scale(Vec3(self.R1[0], self.R1[0], self.R1[0]) * 3.633)
        torus.transform[1] = Matr4.scale(Vec3(.3, 0.7, 0.3)) * Matr4.scale(Vec3(self.R1[0], self.R1[0], self.R1[0]) * 3.1)

        self.ring = self.rnd.prims([sphere, torus], inst_c=len(self.R1))
        self.axis = [Vec3(1, 0, 0), Vec3(2, 0, 1), Vec3(1, 0, 1), Vec3(1, 0, 2), Vec3(0, 0, 1)]

        self.lgh1 = self.rnd.light(pos=Vec3(), color=Vec3(1, 1, 1))
        self.lgh1.is_active = True
        self.lgh2 = self.rnd.light(dir=Vec3(1, 3, 1), color=Vec3(0, 0.2, 0.2))
        self.lgh2.is_active = True

    def update(self):
        """
        Обновление логики юнита, вызывается на каждом кадре.
        Аргументы: нет.
        Выходные данные: нет.
        """
        for i in range(len(self.R1)):
            R0 = self.R1[0]
            rotate = Matr4.rotate(self.timer.time / (self.R1[i] * 15), self.axis[i])
            self.ring.transform[i] = Matr4.rotateY(R2D(-math.pi * i / (len(self.R1) - 1))) * Matr4.scale(Vec3(self.R1[i] / R0, self.R1[i] / R0, self.R1[i] / R0)) * rotate

    def render(self):
        """
        Отрисовка объектов юнита, вызывается на каждом кадре.
        Аргументы: нет.
        Выходные данные: нет.
        """
        self.ring.render()

test_render_unit = TestRenderUnit()