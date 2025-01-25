from units.unit_base import UnitBase
from src.render.rnd import Render
from src.physics.phys import Phys
import pygame
import os
import sys

sys.path.insert(0, "..\\src\\mth\\vec2.py")
import src.mth.vec2 as vec2

class Keyboard:
    """
    Класс, который отвечает за обработку нажатия клавиш на клавиатуре.
    Обрабатываемые клавиши: - все буквы латинского алфавита в нижнем регистре;
                            - правый и левый 'shift';
                            - правый и левый 'ctrl';
                            - 'space';
                            - стрелки вверх, вниз, влево, вправо
    Доступны текущие состояния клавиш и параметр, показывающий, была ли клавиша однократно нажата
    """

    def __init__(self) -> None:
        """
        Установка начальных значений всех состояний
        Аргументы: нет.
        """
        self.keys = {} # текущее состояние клавиатуры
        self.keys_click = {}
        self.__keys_old = {}

        for i in range(97, 123):  # все буквы от a до z
            self.keys[chr(i)] = self.__keys_old[chr(i)] = self.keys_click[chr(i)] = False

        self.keys['shift'] = self.keys['ctrl'] = self.keys[' '] =  False
        self.__keys_old['shift'] = self.__keys_old['ctrl'] = self.__keys_old[' '] = False
        self.keys_click['shift'] = self.keys_click['ctrl'] = self.keys_click[' '] =  False

        self.keys['left'] = self.keys['right'] = self.keys['up'] = self.keys['down'] = False
        self.__keys_old['left'] = self.__keys_old['right'] = self.__keys_old['up'] =  self.__keys_old['down'] = False
        self.keys_click['left'] = self.keys_click['right'] = self.keys_click['up'] = self.keys_click['down'] = False


    def _set_key(self, key : int, value : bool) -> None:
        """
        Изменение состояния клавиши по коду символа:
        Аргументы:
            - код символа нажатой клавиши:
                (int) key;
            - значение, которое требуется установить:
                (bool) value;
        Выходные данные: нет.
        """
        if (97 <= key <= 122) or key == 32:
            self.keys[chr(key)] = value
        elif key == pygame.K_LCTRL or key == pygame.K_RCTRL:
            self.keys['ctrl'] = value
        elif key == pygame.K_LSHIFT or key == pygame.K_RSHIFT:
            self.keys['shift'] = value
        elif key == pygame.K_LEFT:
            self.keys['left'] = value
        elif key == pygame.K_RIGHT:
            self.keys['right'] = value
        elif key == pygame.K_UP:
            self.keys['up'] = value
        elif key == pygame.K_DOWN:
            self.keys['down'] = value

    def _check_clicks(self) -> None:
        """
        Проверка однократного нажатия клавиш. Должна вызываться один раз за кадр:
        Аргументы: нет.
        Выходные данные: нет.
        """
        for key in self.keys_click.keys():
            self.keys_click[key] = self.keys[key] and not self.__keys_old[key]
        self.__keys_old = self.keys.copy()


class Mouse:
    """
    Класс, который отвечает за обработку всех возможных параметров мышки.
    Обрабатываемые параметры мышки: - положение курсора в окне;
                     - относительное перемещение курсора за один кадр;
                     - смещение колеса мышки за кадр;
                     - смещение колеса мышки за всю работу программы;
                     - флаг нажатия правой кнопки мыши;
                     - флаг нажатия левой кнопки мыши;
                     - флаг нажатия колёсика мыши;
    Доступны все перечисленные параметры
    """
    def __init__(self) -> None:
        """
        Установка начальных значений всех параметров
        Аргументы: нет.
        """
        self.cursor_pos = vec2.Vec2()
        self.cursor_delta_pos = vec2.Vec2()
        self.wheel_pos = 0
        self.wheel_delta = 0
        self.is_right_button_pressed = False
        self.is_left_button_pressed = False
        self.is_wheel_pressed = False

    def _set_wheel(self, wheel_delta : int) -> None:
        """
        Обновление параметров колеса.
        Аргументы:
            - относительное смещение колеса в условных единицах:
                (int) wheel_delta;
        Выходные параметры: нет.
        """
        self.wheel_delta = wheel_delta
        self.wheel_pos += wheel_delta

    def _set_cursor(self, cursor_position : tuple[int], offset : tuple[int] = (0, 0)) -> None:
        """
        Обновление позиции курсора.
        Аргументы:
            - текущее положение курсора в пикселях в формате (x, y). Отсчет начинается от верхнего левого угла окна:
                 (tuple[int]) cursor_position;
            - относительное перемещение курсора за кадр в пикселях:
                (tuple[int]) offset;
        Выходные параметры: нет.
        """
        self.cursor_pos.x = cursor_position[0]
        self.cursor_pos.y = cursor_position[1]
        self.cursor_delta_pos.x = offset[0]
        self.cursor_delta_pos.y = offset[1]

    def _reset_deltas(self) -> None:
        """
        Сброс значений относительных изменений за кадр.
        Аргументы: нет.
        Выходные данные: нет.
        """
        self.wheel_delta = 0
        self.cursor_delta_pos.x = 0
        self.cursor_delta_pos.y = 0

    def _set_buttons(self, button : int, value : bool) -> None:
        """
        Изменение состояний нажатия кнопок мышки.
        Аргументы:
            - идентификатор нажатой кнопки в соответствии с pygame:
                 (int) button;
            - значение, которое требуется установить:
                (bool) value;
        Выходные данные: нет.
        """
        if button == 1:
            self.is_left_button_pressed = value
        elif button == 3:
            self.is_right_button_pressed = value
        elif button == 2:
            self.is_wheel_pressed = value


class Timer:
    """
    Класс, который отвечает за все возможные параметры времени (действительно, чем еще заниматься таймеру)
    Доступные параметры:
        - флаг паузы
        - время, отсчитываемое с начала работы программы, без учета паузы
        - время, отсчитываемое с начала работы программы, с учетом паузы
        - промежуток времени между кадрами
        - количество кадров в секунду
    """
    def __init__(self) -> None:
        """
        Определение всех параметров и их начальных значений.
        Аргументы: нет.
        """
        # параметры времени
        self.is_pause = False
        self.is_fps_fixed = False
        self.global_time = 0  # время без учета паузы с начала работы программы
        self.time = 0  # время с учетом паузы
        self.delta_time = 0 # промежуток времени между кадрами
        self.real_fps = 0 # реальное количество кадров в секунду (для статистики)
        self.fps = 0

        # temporary time params
        self.__real_delta_time = 0
        self.__delay = 0
        self.__delay_start = 0
        self.__flag = 1

    def _update(self) -> None:
        """
        Обновление всех указанных параметров времени. Функция должна вызываться одни раз за кадр.
        Аргументы: нет.
        Выходные данные: нет.
        """
        # обработка паузы
        if self.is_pause:
            self.__real_delta_time = 0
            self.delta_time = 0
            # определяем начало паузы
            if self.__flag:
                self.__delay_start = pygame.time.get_ticks()
                self.__flag = 0
        else:
            if not self.__flag:
                self.__delay += pygame.time.get_ticks() - self.__delay_start
                self.__flag = 1
            self.time = pygame.time.get_ticks() - self.__delay
            self.fps, self.delta_time = ((60, 100 / 6) if self.is_fps_fixed else (self.real_fps, self.__real_delta_time))
            self.time = (self.time + self.delta_time - self.__delay if self.is_fps_fixed else (pygame.time.get_ticks() - self.__delay))

        # Во время перетаскивания окна обработка сообщений не работает,
        # поэтому пытаемся отследить этот момент через разницу во времени между кадрами.
        # Это надо убрать при fps меньше 10!
        # if self.__real_delta_time > 100:
        #     self.__delay += self.__real_delta_time
        #     self.delta_time = 2
        #     self.fps = 1 / 0.002

        self.real_fps = 1000 / (self.__real_delta_time + 0.00000001) #self.__cl.get_fps()
        self.__real_delta_time = pygame.time.get_ticks() - self.global_time
        self.global_time = pygame.time.get_ticks()
        # if self.delta_time > 10:
        #     print(self.delta_time, self.real_fps)


class System:
    """
    Класс, который собирает все части проекта (рендер, физика, юниты и прочее) в одно целое.
    Также отвечает за создание окна, обновление таймера и состояний устройств ввода,
        обработку сообщений окна.
    """

    def __init__(self, window_width : int = 800, window_height: int = 800) -> None:
        """
        Инициализация всех параметров.
        Аргументы:
            - ширина и высота создаваемого окна:
                (int) window_width, window_height;
        """
        self.unit_base = UnitBase # глобальные параметры для юнитов
        self.wnd_height = self.unit_base.height = window_height
        self.wnd_width = self.unit_base.width = window_width

        os.environ['SDL_WINDOWS_DPI_AWARENESS'] = 'permonitorv2'
        pygame.init()
        self.screen = pygame.display.set_mode((self.wnd_width, self.wnd_height),
                                flags= pygame.OPENGL | pygame.DOUBLEBUF, vsync=True)

        self.__units = {} # все юниты
        self.rnd = self.unit_base.rnd = Render()
        self.phys = self.unit_base.phys = Phys()
        self.timer = self.unit_base.timer = Timer() # время
        self.keyboard = self.unit_base.keyboard = Keyboard() # состояние клавиатуры
        self.mouse = self.unit_base.mouse = Mouse() # состояние мышки
        self.unit_base.camera = self.rnd.camera
        self.rnd.camera.reshape(window_width, window_height)

    def create_unit(self, name: str, unit: object) -> None:
        """
        Добавление юнита в систему.
        Аргументы:
            - имя юнита:
                (str) name;
            - экземпляр класса юнита:
                (object) unit;
        Выходные данные: нет.
        """
        if name in self.__units.keys():
            print('Unit with such name have already been created. Possible solution: rename your unit')
            return
        self.__units[name] = unit

    def __check_rendering_params(self) -> None:
        """
        Функция, отвечающая за параметры отрисовки, которые распространяются на все юниты (пауза, режим расчета fps и тд)
        Аргументы: нет.
        Выходные данные: нет.
        """
        if self.keyboard.keys['ctrl']:
            if self.keyboard.keys_click['p']:
                self.timer.is_pause = not self.timer.is_pause
            if self.keyboard.keys_click['f']:
                self.timer.is_fps_fixed = not self.timer.is_fps_fixed
            if self.keyboard.keys_click['w']:
                self.rnd.is_wireframe = not self.rnd.is_wireframe


    def run(self) -> None:
        """
        Запуск работы системы (обработка цикла сообщений).
        Аргументы: нет.
        Выходные данные: нет.
        """
        while True:
            self.keyboard._check_clicks()
            self.mouse._reset_deltas()
            self.__check_rendering_params()
            self.timer._update()

            # обработка сообщений
            for event in pygame.event.get():

                if event.type == pygame.MOUSEMOTION:
                    self.mouse._set_cursor(event.pos, event.rel)

                elif event.type == pygame.MOUSEWHEEL:
                    self.mouse._set_wheel(event.y)

                elif event.type == pygame.MOUSEBUTTONDOWN and event.button != 4 and event.button != 5:
                    self.mouse._set_buttons(event.button, True)

                elif event.type == pygame.MOUSEBUTTONUP and event.button != 4 and event.button != 5:
                    self.mouse._set_buttons(event.button, False)

                elif event.type == pygame.KEYDOWN:
                    self.keyboard._set_key(event.key, True)

                elif event.type == pygame.KEYUP:
                    self.keyboard._set_key(event.key, False)

                elif event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            if not self.timer.is_pause:
                self.rnd.update()
                self.phys.update(self.timer.delta_time)
                for unit in self.__units.values():
                    unit.update()
                    unit.render()

            pygame.display.flip()