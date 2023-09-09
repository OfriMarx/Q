from PyQt6.QtGui import QVector2D
from math import sin, cos, atan, pi


def polar_to_algebraic(size, angle):
    return QVector2D(size * cos(angle), size * sin(angle))


def algebraic_to_polar(vector):
    x = vector.x()
    y = vector.y()

    if x == 0:
        return pi / 2
    elif x > 0:
        return atan(y / x)
    else:
        return atan(y / x) + pi


def line_to_vector(line):
    return QVector2D(line.p2() - line.p1())
    

GRAVITY = QVector2D(0, 9.8)
