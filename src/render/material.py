from moderngl import Texture

from src.mth.vec3 import Vec3
from bin.utils.file_reader import FileReader
import moderngl
import numpy

class Material:

    __file_reader = FileReader('.\\bin\\textures\\')

    def __init__(self, name : str, *, ka : Vec3, kd : Vec3, ks : Vec3, ph : float | int, trans : float | int = 0) -> None:
        """
        Инициализация класса материала.
        Аргументы:
            - имя материала:
                (str) name;
            - амбиентная, диффузная, бликовая компоненты цвета:
                (Vec3) ka, kd, ks;
            - коэффициент Фонга:
                (float) ph;
            - прозрачность [0, 1]:
                (float) trans;
        Выходные данные: нет.
        """
        self.ka = ka
        self.kd = kd
        self.ks = ks
        self.ph = ph
        self.trans = trans
        self.textures = []
        self.name = name

    def add_texture(self, tex : str | Texture) -> Texture | None:
        """
        Добавление текстуры в материал.
        Аргументы:
            - имя файла, где хранится текстура: (str) tex,
              созданная текстура: (Texture) tex;
        Выходные данные:
            (Texture) сохраненная текстура.
        """
        if type(tex) == str:
            size, data = Material.__file_reader.read_image(tex)
            if (not size) or (not data):
                print(f'Cannot create "{tex}" texture')
                return None
            texture = moderngl.get_context().texture(size, components=4, data=data)
            texture.build_mipmaps()
            self.textures.append(texture)
            return texture
        else:
            self.textures.append(tex)
            return tex

class Light:
    """
    Инициализация источника освещения.
    Аргументы:
        - позиция источника света или его направление:
            (Vec3) vec;
        - является ли переданный вектор позицией источника света:
            (bool) is_position;
        - цвет освещения:
            (Vec3) color;
    Выходные данные: нет.
    """
    def __init__(self, vec : Vec3 = Vec3(), is_position : bool = True, color : Vec3 = Vec3(1, 1, 1)) -> None:
        self.vector = Vec3(vec.x, vec.y, vec.z)
        self.is_position = is_position
        self.color = Vec3(color.x, color.y, color.z)
        self.is_active = False

    def render(self) -> None:
        """
        Активация источника освещения.
        Аргументы: нет.
        Выходные данные: нет.
        """
        self.is_active = True


material_table = {
    "black plastic": {"name" : "black plastic", 'ka' : Vec3(), 'kd' : Vec3(0.01, 0.01, 0.01),
                        'ks' : Vec3(0.5, 0.5, 0.5), 'ph' : 32.4},
    "brass" : {'name' : "brass", 'ka' : Vec3(0.329412, 0.223529, 0.027451), 'kd' : Vec3(0.780392, 0.568627, 0.113725),
                        'ks' : Vec3(0.992157, 0.941176, 0.807843), 'ph' : 27.8974},
    "bronze" : {'name' : "bronze", 'ka' : Vec3(0.2125, 0.1275, 0.054), 'kd' : Vec3(0.714, 0.4284, 0.18144),
                        'ks' : Vec3(0.393548, 0.271906, 0.166721), 'ph' : 25.6},
    "default" : {'name' : "default", 'ka' : Vec3(0.05, 0.05, 0.05) / 3, 'kd' : Vec3(0.35, 0.35, 0.35) / 8,
                        'ks' : Vec3(0.55, 0.55, 0.55) * 1.4, 'ph' : 5},
    "chrome" : {'name' : "chrome", 'ka' : Vec3(0.25, 0.25, 0.25), 'kd' : Vec3(0.4, 0.4, 0.4),
                        'ks' : Vec3(0.774597, 0.774597, 0.774597), 'ph' : 76.8},
    "copper" : {'name' : "copper", 'ka' : Vec3(0.19125, 0.0735, 0.0225), 'kd' : Vec3(0.7038, 0.27048, 0.0828),
                        'ks' : Vec3(0.256777, 0.137622, 0.086014), 'ph' : 12.8},
    "gold" : {'name' : 'gold', 'ka' : Vec3(0.24725, 0.1995, 0.0745), 'kd' : Vec3(0.75164, 0.60648, 0.22648),
                        'ks' : Vec3(0.628281, 0.555802, 0.366065), 'ph' : 51.2},
    "peweter": {'name' : "peweter", 'ka' : Vec3(0.10588, 0.058824, 0.113725), 'kd' : Vec3(0.427451, 0.470588, 0.541176),
                        'ks' : Vec3(0.3333, 0.3333, 0.521569), 'ph' : 9.84615},
    "silver" : {'name' : "silver", 'ka' : Vec3(0.19225, 0.19225, 0.19225), 'kd' : Vec3(0.50754, 0.50754, 0.50754),
                        'ks' : Vec3(0.508273, 0.508273, 0.508273), 'ph' : 51.2},
    "polished silver" : {'name' : "polished silver", 'ka' : Vec3(0.23125, 0.23125, 0.23125), 'kd' : Vec3(0.2775, 0.2775, 0.2775),
                        'ks' : Vec3(0.773911, 0.773911, 0.773911), 'ph' : 89.6},
    "turquoise" : {'name' : "turquoise", 'ka' : Vec3(0.1, 0.18725, 0.1745), 'kd' : Vec3(0.396, 0.74151, 0.69102),
                        'ks' : Vec3(0.297254, 0.30829, 0.306678), 'ph' : 12.8},
    "ruby" : {'name' : "ruby", 'ka' : Vec3(0.1745, 0.01175, 0.1175), 'kd' : Vec3(0.61424, 0.04136, 0.04136),
                        'ks' : Vec3(0.727811, 0.626959, 0.626959), 'ph' : 76.8},
    "polished gold" : {'name' : "polished gold", 'ka' : Vec3(0.24725, 0.2245, 0.0645), 'kd' : Vec3(0.34615, 0.3143, 0.0903),
                        'ks' : Vec3(0.797357, 0.723991, 0.208006), 'ph' : 83.2},
    "polished bronze" : {'name' : "polished bronze", 'ka' : Vec3(0.25, 0.148, 0.06475), 'kd' : Vec3(0.4, 0.2368, 0.1036),
                         'ks' : Vec3(0.774597, 0.458561, 0.200621), 'ph' : 76.8},
    "polished copper" : {'name' : "polished copper", 'ka' : Vec3(0.2295, 0.08825, 0.0275), 'kd' : Vec3(0.5508, 0.2118, 0.066),
                         'ks' : Vec3(0.580594, 0.223257, 0.0695701), 'ph' : 76.2},
    "jade" : {'name' : "jade", 'ka' : Vec3(0.135, 0.2225, 0.1575), 'kd' : Vec3(0.135, 0.2225, 0.1575),
                         'ks' : Vec3(0.316228, 0.316228, 0.316228), 'ph' : 12.8},
    "obsidian" : {'name' : "obsidian", 'ka' : Vec3(0.05375, 0.05, 0.06625), 'kd' : Vec3(0.18275, 0.17, 0.22525),
                         'ks' : Vec3(0.332741, 0.328634, 0.346435), 'ph' : 38.4},
    "pearl" : {'name' : "pearl", 'ka' : Vec3(0.25, 0.20725, 0.20725), 'kd' : Vec3(1, 0.829, 0.829),
                         'ks' : Vec3(0.296648, 0.296648, 0.296648), 'ph' : 11.264},
    "emerald" : {'name' : "emerald", 'ka' : Vec3(0.0215, 0.1745, 0.0215), 'kd' : Vec3(0.07568, 0.61424, 0.07568),
                         'ks' : Vec3(0.633, 0.727811, 0.633), 'ph' : 76.8},
    "black rubber" : {'name' : "black rubber", 'ka' : Vec3(0.02, 0.02, 0.02), 'kd' : Vec3(0.01, 0.01, 0.01),
                         'ks' : Vec3(0.4, 0.4, 0.4), 'ph' : 10},
}