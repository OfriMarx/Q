from utils import GRAVITY

from PyQt6.QtGui import QVector2D
from PyQt6.QtCore import QPointF, QRectF, QSizeF, QLineF
from PyQt6.QtGui import QBrush, QPen, QColor

from itertools import product


class Shape(object):
    def __init__(self, x, y, m):
        self.point = QPointF(x, y)
        self.velocity = QPointF(0, 0)
        self.mass = m
        self.forces = []

    def draw(self, painter):
        raise NotImplementedError()

    def to_lines(self):
        raise NotImplementedError()

    def intersects(self, shape):
        # TODO: fix problems. very slim objects can pass through
        for comb in product(self.to_lines(), shape.to_lines()):
            # print(comb)
            intersection = comb[0].intersects(comb[1])[0]
            # print(intersection)
            if intersection == QLineF.IntersectionType.BoundedIntersection:
                return comb
            elif intersection == QLineF.IntersectionType.NoIntersection:
                if QLineF(comb[0].p1(), comb[1].p1()).intersects(comb[0])[0] == QLineF.IntersectionType.NoIntersection:
                    return comb
        return False

    def update(self, time_passed):
        time_passed *= 5
        force = sum(self.forces, start=QVector2D(0, 0))
        x_accl = force.x() / self.mass
        y_accl = force.y() / self.mass
        self.velocity += QPointF(x_accl * time_passed, y_accl * time_passed)
        self.point += QPointF(self.velocity.x() * time_passed, self.velocity.y() * time_passed)


class Circle(Shape):
    def __init__(self, x, y, m, r):
        super().__init__(x, y, m)
        self.radius = r

    def draw(self, painter):
        painter.setPen(QPen(QColor("red"), 2))
        painter.setBrush(QBrush(QColor("red")))
        painter.drawEllipse(self.point, self.radius, self.radius)

    def to_lines(self):
        x, y, r = self.point.x(), self.point.y(), self.radius
        return [QLineF(x - r, y - r, x + r, y - r), QLineF(x + r, y - r, x + r, y + r), QLineF(x + r, y + r, x - r, y + r), QLineF(x - r, y + r, x - r, y - r)]


class Ball(Circle):
    def __init__(self, *args):
        super().__init__(*args)
        self.forces.append(GRAVITY * self.mass)


class Rect(Shape):
    def __init__(self, x, y, m, w, h):
        super().__init__(x, y, m)
        self.size = QSizeF(w, h)

    def draw(self, painter):
        painter.setPen(QPen(QColor("green"), 2))
        painter.setBrush(QBrush(QColor("green")))
        painter.drawRect(QRectF(self.point, self.size))

    def to_lines(self):
        x, y, w, h = self.point.x(), self.point.y(), self.size.width(), self.size.height()
        return [QLineF(x, y, x + w, y), QLineF(x + w, y, x + w, y + h), QLineF(x + w, y + h, x, y + h), QLineF(x, y + h, x, y)]


class Box(Rect):
    def __init__(self, *args):
        super().__init__(*args)
        self.forces.append(GRAVITY * self.mass) 
