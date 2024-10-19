"""
Модуль с дополнительными общими математическими функциями, которые логически не относятся к
какому-либо из написанных классов
"""
import math

# перевод градусов в радианы
D2R = lambda angle_in_degree: angle_in_degree * math.pi / 180

# перевод радиан в градусы
R2D = lambda angle_in_radian: angle_in_radian * 180 / math.pi
