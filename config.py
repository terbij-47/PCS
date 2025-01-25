#*** уберите это, если пакеты установлены
from os import system as install
install('pip install numpy pygame moderngl pillow')
#***

from src.system import System
stm = System(1000, 1000)
# Специальные сочетания клавиш:
# 'ctrl' + 'p' -> поставить все на паузу / убрать паузу
# 'ctrl' + 'w' -> включить / выключить wireframe
# 'ctrl' + 'f' -> переход на фиксированное fps = 60. Использовать в том случае,
#           когда время между кадрами слишком большое, что не позволяет корректно обновить что-либо

import units.camera_unit as cam
stm.create_unit("camera control unit", cam.camera_control)

# import units.render_test as urt
# stm.create_unit('render test', urt.test_render_unit)

import units.cloth_unit as cloth
stm.create_unit('cloth unit', cloth.cloth_unit)

stm.run()