from units.unit_base import *

class CameraUnit(UnitBase):
    """
    Юнит управления камерой.
    """
    def __init__(self) -> None:
        """
        Конструктор класса.
        Аргументы: нет.
        Выходные данные: нет.
        """
        self.camera.set(Vec3(5, 10 / 4, 25 / 8), Vec3(), Vec3(0, 1, 0))

        self.camera_speed = 1.2
        self.pos = self.camera.loc.copy()
        self.dir = self.camera.dir.copy()

        self.pitch = math.pi / 2 - math.acos(self.dir * Vec3(0, 1, 0))
        delta = Vec3(self.dir.x, 0, self.dir.z)
        self.yaw = math.atan2(~delta * Vec3(0, 0, 1), ~delta * Vec3(1, 0, 0))

    def update(self):
        """
        Обновление отдельных параметров камеры.
        Аргументы: нет.
        Выходные данные: нет.
        """
        delta = Vec3()
        if self.keyboard.keys['w'] and not self.keyboard.keys['ctrl']:
            delta += self.camera.dir * self.timer.delta_time / 1000 * self.camera_speed
        if self.keyboard.keys['s']:
            delta -= self.camera.dir * self.timer.delta_time / 1000 * self.camera_speed
        if self.keyboard.keys['a']:
            delta -= self.camera.right * self.timer.delta_time / 1000 * self.camera_speed
        if self.keyboard.keys['d']:
            delta += self.camera.right * self.timer.delta_time / 1000 * self.camera_speed
        self.pos += delta

        if self.mouse.is_left_button_pressed:
            self.pitch -= self.mouse.cursor_delta_pos.y / 1000
            self.yaw += self.mouse.cursor_delta_pos.x / 1000

            if self.pitch > D2R(89):
                self.pitch = D2R(89)
            if self.pitch < D2R(-89):
                self.pitch = D2R(-89)

            self.dir = ~Vec3(
                math.cos(self.pitch) * math.cos(self.yaw),
                math.sin(self.pitch),
                math.cos(self.pitch) * math.sin(self.yaw)
            )

        self.pos += self.camera.dir * self.timer.delta_time / 1000 * self.camera_speed * 3 * self.mouse.wheel_delta


    def render(self):
        """
         Обновление камеры сцены.
         Аргументы: нет.
         Выходные данные: нет.
         """
        self.camera.set(self.pos, self.pos + self.dir, Vec3(0, 1, 0))


camera_control = CameraUnit()
