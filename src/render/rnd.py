import moderngl
from moderngl import Texture

from src.mth.camera import Camera
from src.render.material import Light
from src.render.prim import *

class Render:
    MAX_LIGHT_COUNT = 20

    def __init__(self) -> None:
        """
        Конструктор класса.
        Аргументы: нет.
        Выходные данные: нет.
        """
        self.is_wireframe = False
        self.mtl_table = material_table
        self.camera = Camera()

        self.__shaders = {}
        self.__textures = {}
        self.__prims = []
        self.__lights = []
        self.__ctx = moderngl.get_context()
        self.__ctx.enable(moderngl.DEPTH_TEST )

        # common render ubo
        self.__prim_for_ubo = self.prim(self.geom(vertices=[]))
        self.__camera_ubo = self.__prim_for_ubo.create_ubo(0, 20)
        self.__light_ubo = self.__prim_for_ubo.create_ubo(3, 8 * self.MAX_LIGHT_COUNT)


    def shader(self, name : str = 'default', pattern : str = 'pos, norm, tex_c') -> Shader | None:
        """
        Функция создания шейдера.
        Аргументы:
            - название директории, в которой находятся файлы шейдера:
                (str) name;
            - формат атрибутов вершин примитива:
                (str) pattern;
        Выходные данные:
            (Shader) загруженный шейдер
        """
        if name in self.__shaders.keys():
            return self.__shaders[name]

        new_shd = Shader(name, pattern)
        if new_shd.prg == None:
            return None
        self.__shaders[name] = new_shd
        return new_shd

    def geom(self, *, type : str = None, vertices : None | list[Vertex] = None,
                        indices : None | list[int] = None, geom_type : int = moderngl.TRIANGLE_STRIP, **kwargs) -> None | Geometry:
        """
        Функция создания геометрии.
        Аргументы:
            - название директории, в которой находятся файлы шейдера:
                (str) name;
            - формат атрибутов вершин примитива:
                (str) pattern;
        Выходные данные:
            (Shader) загруженный шейдер
        """
        geom = Geometry()
        if vertices:
            geom.vertex_array = vertices
            if indices:
                geom.index_array = indices
            geom.geom_type = geom_type
        elif type:
            if type == 'grid':
                geom.grid(kwargs['w'], kwargs['h'])
            elif type == 'sphere':
                geom.sphere(kwargs['w'], kwargs['h'])
            elif type == 'torus':
                geom.torus(kwargs['r'], kwargs['w'], kwargs['h'])
            elif type == 'box':
                geom.box()
            elif type == 'plane':
                geom.plane()
            else:
                print(f'Cannot create geometry. Unknown geometry type "{type}"')
                return None
        return geom

    def prim(self, geometry : Geometry, *, shader : Shader | None = None, material : Material | None = None, inst_c : int = 1) -> Prim | None:
        """
        Создание примитива из геометрии.
        Аргументы:
            - заданная геометрия (может быть пустой):
                (Geometry) geometry;
            - шейдер примитива:
                (Shader) shader;
            - материал примитива:
                (Material) material;
            - количество копий примитива (instancing):
                (int) inst_c;
        Выходные данные:
            (Prim) созданный примитив
        """
        if not shader:
            shader = self.shader()
            if not shader:
                print('Cannot create primitive. Shader was not loaded.')
                return None
        if not material:
            material = self.material()
        prim = Prim(geometry= geometry, shader= shader, material= material, instance_count=inst_c)
        self.__prims.append(prim)
        return prim


    def prims(self, primitives : list[Prim], *, inst_c : int = 1) -> PrimCollection:
        """
        Создание коллекции из примитивов.
        Аргументы:
            - список примитивов:
                (list[Prim]) primitives;
            - количество копий коллекции (instancing):
                (int) inst_c;
        Выходные данные:
            (PrimCollection) созданная коллекция примитивов.
        """
        collection = PrimCollection(primitives, inst_c=inst_c)
        return collection

    def material(self, name : str = 'default', *, ka : Vec3 = Vec3(), kd : Vec3 = Vec3(), ks : Vec3 = Vec3(),
                 ph : float | int = 0, trans : float | int = 0, tex2 : tuple[str] = ()) -> Material | None:
        """
        Создание материала.
        Аргументы:
            - имя материала:
                (str) name;
            - амбиентная, диффузная, бликовая компоненты цвета:
                (Vec3) ka, kd, ks;
            - коэффициент Фонга:
                (float) ph;
            - прозрачность [0, 1]:
                (float) trans;
            - кортеж имен файлов текстур материалов:
                (tuple[str]) tex2;
        Выходные данные:
            (Material) созданный материал.
        """
        mtl = None
        if name in self.mtl_table.keys():
            mtl = Material(**self.mtl_table[name])
        else:
            mtl = Material(name, ka=ka, kd=kd, ks=ks, ph=ph, trans=trans)
            self.mtl_table[name] = {'name' : name, 'ka':ka, 'kd':kd, 'ks':ks, 'ph':ph, 'trans':trans}
        for key in tex2:
            if key in self.__textures.keys():
                mtl.add_texture(self.__textures[key])
            else:
                self.__textures[key] = mtl.add_texture(key)
        return mtl

    def light(self, *, pos : Vec3 = Vec3(0, 10, 0), dir : Vec3 = None,
                     color : Vec3 = Vec3(1, 1, 1)) -> Light:
        """
        Создание источника света.
        Аргументы:
                - позиция источника света:
                    (Vec3) pos;
            ИЛИ
                - направление освещения:
                    (Vec3) dir;
            - цвет освещения:
                (Vec3) color;
        Выходные данные:
            (Light) источник света.
        """
        lgh = Light(pos, True, color) if not dir else Light(~dir, False, color)
        self.__lights.append(lgh)
        return lgh

    def update(self) -> None:
        """
        Обновление глобальных параметров рендера.
        Аргументы: нет.
        Выходные данные: нет.
        """
        for shd in self.__shaders.values():
            shd.update()

        self.__ctx.wireframe = self.is_wireframe
        self.__ctx.clear()

        # camera ubo
        self.__camera_ubo[0:16] = self.camera.view_proj.to_tuple()
        self.__camera_ubo[16] = self.camera.loc.x
        self.__camera_ubo[17]= self.camera.loc.y
        self.__camera_ubo[18] = self.camera.loc.z

        offset = 0
        for lgh in self.__lights:
            if offset / 8 > Render.MAX_LIGHT_COUNT:
                break
            if lgh.is_active:
                self.__light_ubo[offset + 0] = lgh.vector.x
                self.__light_ubo[offset + 1] = lgh.vector.y
                self.__light_ubo[offset + 2] = lgh.vector.z
                self.__light_ubo[offset + 3] = lgh.is_position

                self.__light_ubo[offset + 4] = lgh.color.x
                self.__light_ubo[offset + 5] = lgh.color.y
                self.__light_ubo[offset + 6] = lgh.color.z

                offset += 8
        self.__light_ubo[7] = (offset) // 8
        self.__prim_for_ubo.render()