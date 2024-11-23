# импорты для остальных юнитов
from src.mth.camera import *
from src.mth.vec4 import Vec4
from src.mth.vec2 import Vec2
from src.mth.mth import *

class UnitBase:
    # параметры, доступные в каждом юните
    rnd = None
    phys = None
    timer = None
    keyboard = None
    mouse = None
    ctx = None  # временное решение
    w = 0
    h = 0
    camera = None

    def __init__(self):
        """
        Конструктор-заглушка класса.
        Аргументы: нет.
        """
        pass

    def update(self):
        """
        Обновление логики юнита, вызывается на каждом кадре.
        Аргументы: нет.
        Выходные данные: нет.
        """
        print("Метод 'update' базового класса 'UnitBase' не был замещен", flush=True)


    def render(self):
        """
        Отрисовка объектов юнита, вызывается на каждом кадре.
        Аргументы: нет.
        Выходные данные: нет.
        """
        print("Метод 'render' базового класса 'UnitBase' не был замещен", flush=True)
