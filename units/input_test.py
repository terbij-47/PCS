from units.unit_base import *  # должно быть в каждом юните
import pygame  # временное решение

class TestInputUnit(UnitBase):
    """
    Тестовый юнит для проверки работы системы, клавиатуры, мышки, таймера.
    Наследование базового класса обязательно.
    """
    def __init__(self):
        """
        Конструктор класса.
        Можно оставить пустым, тк в момент создания экземпляра класса все системные переменные self.* еще не проинициализированы
        """
        super().__init__()

    def create(self):
        """
        Создание юнита, вызывается после инициализации всех остальных систем.
        Аргументы: нет.
        Выходные данные: нет.
        """
        self.R = (self.w + self.h) * 3 / 16
        self.alpha = 2
        self.center = Vec2(self.w / 2, self.h / 2)
        self.offsets = [(D2R(0), 50), (D2R(-20), 45), (D2R(-20), 40), (D2R(-20), 35), (D2R(-20), 30),
                        (D2R(-20), 25), (D2R(-20), 20), (D2R(-20), 15), (D2R(-20), 10), (D2R(-20), 5)]
        self.positions = [i for i in range(0, len(self.offsets))]


    def update(self):
        """
        Обновление логики юнита, вызывается на каждом кадре.
        Аргументы: нет.
        Выходные данные: нет.
        """
        offset = 0
        if self.keyboard.keys_click['up']:
            self.R += 10
        if self.keyboard.keys_click['down']:
            self.R -= 10
        if self.mouse.is_left_button_pressed:
            self.center += self.mouse.cursor_delta_pos.copy()
        self.alpha += self.mouse.wheel_delta / 10
        self.alpha = max(0, self.alpha)

        for i, off in enumerate(self.offsets):
            offset += off[0]
            self.positions[i] = \
                    Vec2(math.sin(self.timer.time / 1000 / 2 + offset),
                         -math.cos(self.timer.time / 1000 / 2 + offset)) * self.R + self.center

    def render(self):
        """
        Отрисовка объектов юнита, вызывается на каждом кадре.
        Аргументы: нет.
        Выходные данные: нет.
        """
        for i, off in enumerate(self.offsets):
            rel = self.positions[i] - self.center
            r =  int(255 * ((math.sin(rel.x * math.pi / self.R) / 2) + 0.5))
            g =  int(255 * ((math.sin(rel.y * math.pi / self.R) / 2) + 0.5))
            b =  int(255 * ((math.sin(r * 0.01) + math.cos(g * 0.01) + 2) / 4))
            pygame.draw.circle(self.ctx, (b, g, g), self.positions[i].to_tuple(), off[1] * self.alpha, 0)

test_input_unit = TestInputUnit()