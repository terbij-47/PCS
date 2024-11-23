from src.render.geom import *
from src.render.shader import Shader
from src.render.material import Material, material_table
import numpy as nmp

from src.mth.matr4 import Matr4

class Prim:
    layouts = {'pos' : (0, '3f'), 'norm': (1, '3f'), 'tex_c': (2, '2f'), 'color': (3, '4f')}

    def __init__(self, *, geometry : Geometry, shader : Shader, material : Material, instance_count : int) -> None:
        """
        Инициализация класса примитива.
        Аргументы:
            - геометрия примитива:
                (Geometry) geometry;
            - шейдер:
                (Shader) shader;
            - материал примитива:
                (Material) material;
            - количество копий:
                (int) instance_count;
        Выходные данные: нет.
        """
        self.ctx = moderngl.get_context()
        self.geom = geometry  # геометрия
        self.shd = shader
        self.mtl = material
        self.vao = None  # vertex_array
        self.instances_count = instance_count
        self.transform = [Matr4() for i in range(instance_count)]

        self.__ubo_id_dict = {}
        self._instance_data = self.create_ubo(1, self.instances_count * 32)
        self.__create()

    def create_ubo(self, binding_point : int, amount_of_float : int) -> list:
        """
        Создание UBO.
        Аргументы:
            - точка привязки UBO на шейдере:
                (int) binding_point;
            - количество float, записываемых в UBO:
                (int) amount_of_float;
        Выходные данные:
            (list) список, привязанный к UBO.
        """
        index = Shader.create_ubo(binding_point, amount_of_float)
        self.__ubo_id_dict[binding_point] = index
        return Shader.uniform_buffers[index]['data']

    def release_ubo(self, binding_point : int) -> None:
        """
        Удаление UBO.
        Аргументы:
            - точка привязки UBO на шейдере:
                (int) binding_point;
        Выходные данные: нет.
        """
        Shader.uniform_buffers.pop(self.__ubo_id_dict[binding_point], None)
        self.__ubo_id_dict.pop(binding_point, None)

    def __create(self) -> None:  # must be updated
        """
        Загрузка данных примитива в память.
        Аргументы: нет.
        Выходные данные: нет.
        """
        if len(self.geom.vertex_array):
            # у нас есть вертексы, будем их обрабатывать
            patterns = self.shd.layout_patterns

            layout_data = []
            for v in self.geom.vertex_array:
                for pat in patterns:
                    layout_data.extend( v.to_array()[Vertex.offset[pat][0] : Vertex.offset[pat][1]] )
            layout_buff = self.ctx.buffer( nmp.array(layout_data, dtype='f4') )
            bindings = []
            for p in patterns:
                bindings.append(Prim.layouts[p][0])
            # есть еще и индексы
            if self.geom.index_array:
                id_buff = self.ctx.buffer(nmp.array(self.geom.index_array, dtype='i4'))
                self.vao = self.ctx.vertex_array(self.shd.prg, [
                    layout_buff.bind(*bindings)
                    ], index_buffer= id_buff, mode= self.geom.geom_type)
            else:
                self.vao = self.ctx.vertex_array(self.shd.prg, [
                    layout_buff.bind(*bindings)
                    ], mode= self.geom.geom_type)
        # нет ничего
        else:
            vert_count = max(1, self.geom.vertex_count)
            self.vao = self.ctx.vertex_array(self.shd.prg, [], mode=moderngl.POINTS)
            self.vao.vertices = vert_count
        # self.vao.instances = 2

    def render(self, *, add_translate : list[Matr4] | None = None, add_instance : int = 1) -> None:
        """
        Отрисовка примитивов и обновление UBO.
        Аргументы:
            - дополнительная матрица преобразования:
                (Matr4) add_translate;
            - количество групп таких примитивов:
                (int) add_instance;
        Выходные данные: нет.
        """
        # update view params
        if type(self.transform) == Matr4:
            self.transform = [self.transform]

        # разные примитивы могут использовать один шейдер
        self.shd['ka'] = self.mtl.ka.to_tuple()
        self.shd['kd'] = self.mtl.kd.to_tuple()
        self.shd['ks'] = self.mtl.ks.to_tuple()
        self.shd['ph'] = self.mtl.ph
        self.shd['trans'] = self.mtl.trans
        self.shd['instance_count'] = int(self.instances_count * add_instance)

        for i in range(len(self.mtl.textures)):
            self.shd[f'texture_{i}'] = i
            self.mtl.textures[i].use(location=i)
        self.shd['is_texture'] = len(self.mtl.textures)

        # set instances matrices
        if not add_translate:
            add_translate = [Matr4()]
        k = 0
        for matr in add_translate:
            for i in range(self.instances_count):
                self._instance_data[k : k + 16] = (self.transform[i] * matr).to_tuple()
                self._instance_data[k + 16 : k + 32] = (self.transform[i] * matr).inverse().transpose().to_tuple()
                k += 32

        # update uniform buffers
        for i in self.__ubo_id_dict.values():
            Shader.update_ubo(i)

        self.vao.render(instances=self.instances_count * add_instance)


class PrimCollection:

    def __init__(self, prims : list, *, inst_c : int) -> None:
        """
        Инициализация коллекции примитивов.
        Аргументы:
            - список примитивов коллекции:
                (list) prims;
            - количество копий данной коллекции:
                (int) inst_c;
        Выходные данные: нет.
        """
        self.prims = prims
        self.instance_count = inst_c
        self.transform = [Matr4() for i in range(self.instance_count)]
        if inst_c != 1:
            for prim in prims:
                prim.release_ubo(1)
                prim._instance_data = prim.create_ubo(1, prim.instances_count * inst_c * 32)

    def render(self) -> None:
        """
        Отрисовка коллекции примитивов.
        Аргументы: нет.
        Выходные данные: нет.
        """
        if type(self.transform) == Matr4:
            self.transform = [self.transform]

        for prim in self.prims:
            prim.render(add_instance=self.instance_count, add_translate=self.transform)