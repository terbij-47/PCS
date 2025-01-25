from moderngl import Buffer
from bin.utils.file_reader import FileReader
import moderngl
import numpy as nmp

class Shader:
    reader = FileReader('.\\bin\\shaders\\')
    # формат хранения: {id : {binding_point : .., data : .., ubo : ..}}
    uniform_buffers = {}
    __max_id = 0

    @classmethod
    def create_ubo(cls, binding_point : int, amount_of_float : int) -> int:
        """
        Создание UBO.
        Аргументы:
            - точка привязки UBO на шейдере:
                (int) binding_point;
            - количество float, записываемых в UBO:
                (int) amount_of_float;
        Выходные данные:
            (int) индекс UBO в общей таблице.
        """
        cls.uniform_buffers[cls.__max_id] = {
            'binding_point' : binding_point,
            'data' : nmp.array([ 0. for i in range(amount_of_float)], dtype='f4'),
            'ubo' : moderngl.get_context().buffer(bytearray(4 * amount_of_float))
        }
        cls.__max_id += 1
        return cls.__max_id - 1

    @classmethod
    def update_ubo(cls, ubo_id : int) -> None:
        """
        Обновление UBO.
        Аргументы:
            - индекс UBO в таблице:
                (int) ubo_id;
        Выходные данные: нет.
        """
        bind = cls.uniform_buffers[ubo_id]['binding_point']
        data = cls.uniform_buffers[ubo_id]['data']
        ubo = cls.uniform_buffers[ubo_id]['ubo']
        ubo.write(data)
        ubo.bind_to_uniform_block(binding=bind)

    def __init__(self, shader_name : str = 'default', pattern : str = 'pos, norm, tex_c, color') -> None:
        """
        Создание шейдера.
        Аргументы:
            - имя директории шейдера:
                (str) shader_name;
            - формат входных данных шейдера:
                (str) pattern;
        Выходные данные: нет.
        """
        self.name = shader_name
        self.ctx = moderngl.get_context()

        self.layout_patterns = []
        patterns = (pattern.split(', '))
        for p in patterns:
            if p in ('pos', 'norm', 'tex_c', 'color'):
                self.layout_patterns.append(p)

        self.uniforms_name = []
        self.ubo_id_lst = []

        self.__shaders = {
            'vertex_shader': Shader.reader.read_file(shader_name + '\\vert.glsl'),
            'tess_control_shader': Shader.reader.read_file(shader_name + '\\ctrl.glsl'),
            'tess_evaluation_shader': Shader.reader.read_file(shader_name + '\\eval.glsl'),
            'geometry_shader': Shader.reader.read_file(shader_name + '\\geom.glsl'),
            'fragment_shader': Shader.reader.read_file(shader_name + '\\frag.glsl')
        }

        self.__update_time = {
            'vertex_shader': int(Shader.reader.last_update_time(shader_name + '\\vert.glsl')),
            'tess_control_shader': int(Shader.reader.last_update_time(shader_name + '\\ctrl.glsl')),
            'tess_evaluation_shader': int(Shader.reader.last_update_time(shader_name + '\\eval.glsl')),
            'geometry_shader': int(Shader.reader.last_update_time(shader_name + '\\geom.glsl')),
            'fragment_shader': int(Shader.reader.last_update_time(shader_name + '\\frag.glsl'))
        }

        # delete shader if it doesn't exist
        for key, value in dict(self.__shaders).items():
            if not value:
                del self.__shaders[key]

        if len(self.__shaders) == 0:
            print(f'Cannot create "{shader_name}" shader')
            self.prg = None
            return

        # create openGl shader program
        self.prg = self.ctx.program(**self.__shaders)

    def update(self):
        """
        Обновление шейдера, чтоб можно было изменять его во время работы программы.
        Аргументы: нет.
        Выходные данные: нет.
        """
        is_changed = False
        time = int(Shader.reader.last_update_time(self.name + '\\vert.glsl'))
        if time != self.__update_time['vertex_shader']:
            self.__update_time['vertex_shader'] = time
            self.__shaders['vertex_shader'] = Shader.reader.read_file(self.name + '\\vert.glsl')
            is_changed = True
        time = int(Shader.reader.last_update_time(self.name + '\\ctrl.glsl'))
        if time != self.__update_time['tess_control_shader']:
            self.__update_time['tess_control_shader'] = time
            self.__shaders['tess_control_shader'] = Shader.reader.read_file(self.name + '\\ctrl.glsl')
            is_changed = True
        time = int(Shader.reader.last_update_time(self.name + '\\eval.glsl'))
        if time != self.__update_time['tess_evaluation_shader']:
            self.__update_time['tess_evaluation_shader'] = time
            self.__shaders['tess_evaluation_shader'] = Shader.reader.read_file(self.name + '\\eval.glsl')
            is_changed = True
        time = int(Shader.reader.last_update_time(self.name + '\\geom.glsl'))
        if time != self.__update_time['geometry_shader']:
            self.__update_time['geometry_shader'] = time
            self.__shaders['geometry_shader'] = Shader.reader.read_file(self.name + '\\geom.glsl')
            is_changed = True
        time = int(Shader.reader.last_update_time(self.name + '\\frag.glsl'))
        if time != self.__update_time['fragment_shader']:
            self.__update_time['fragment_shader'] = time
            self.__shaders['fragment_shader'] = Shader.reader.read_file(self.name + '\\frag.glsl')
            is_changed = True

        if is_changed:
            # delete shader if it doesn't exist
            for key, value in dict(self.__shaders).items():
                if not value:
                    del self.__shaders[key]
            if len(self.__shaders) == 0:
                print(f'Cannot create "{self.name}" shader')
                self.prg = None
                return
            self.prg.release()
            self.prg = self.ctx.program(**self.__shaders)


    def __setitem__(self, key : str, value : int | float | list[float] | tuple[float]) -> None:
        """
        Оператор [] - изменение юниформов шейдера.
        Аргументы:
            - имя юниформа:
                (str) key;
            - новое значение юниформа:
                (int | float | list[float] | tuple[float]) value;
        Выходные данные: нет.
        """
        if self.prg.get(key, None):
            if key not in self.uniforms_name:
                self.uniforms_name.append(key)
            self.prg[key] = value


    # def __getitem__(self, key : str):
    #     """
    #     Оператор [] - получение значений юниформов.
    #     Аргументы:
    #         - имя юниформа:
    #             (str) key;
    #     Выходные данные:
    #         (float | int | tuple[float]) значение юниформа.
    #     """
    #     return self.prg.get(key, None)