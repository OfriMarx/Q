from shapes import Ball, Rect, Circle, Box
from utils import line_to_vector, algebraic_to_polar

from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtGui import QPainter, QVector2D
from PyQt6.QtCore import QTimer

from time import time
from itertools import combinations
from math import pi


class Window(QMainWindow):
    TITLE = "Q"
    SIZE = (500, 500)
    START = (500, 150)

    def __init__(self):
        super().__init__()
        self.init_window()
        self.init_loop()

    def init_window(self):
        self.setWindowTitle(Window.TITLE)
        # TODO: open at the middle of the screen
        self.setGeometry(*Window.START, *Window.SIZE)
        self.show()

    def init_loop(self):
        self.shapes = []

        self.last = time()
        self.current = time()

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_shapes)
        self.timer.start(1)

    def update_shapes(self):
        self.last, self.current = self.current, time()
        time_passed = self.current - self.last

        # TODO: fix position of object if got into another object
        for shape_pair in combinations(self.shapes, 2):
            intersecting_lines = shape_pair[0].intersects(shape_pair[1])
            if intersecting_lines:
                beta_angle = algebraic_to_polar(line_to_vector(intersecting_lines[1]))
                alpha_angle = algebraic_to_polar(QVector2D(shape_pair[0].velocity))
                gamma_angle = 2 * pi - alpha_angle + 2 * beta_angle
                print(alpha_angle, gamma_angle)

                m1, v1 = shape_pair[0].mass, shape_pair[0].velocity.y()
                m2, v2 = shape_pair[1].mass, shape_pair[1].velocity.y()
                v3 = (m1 * v1 - v1 * m2 + 2 * m2 * v2) / (m1 + m2)
                v4 = (2 * m1 * v1 - m1 * v2 + m2 * v2) / (m1 + m2)
                shape_pair[0].velocity.setY(v3)
                shape_pair[1].velocity.setY(v4)


        for shape in self.shapes:
            shape.update(time_passed)

        self.update()

    def add_shape(self, shape):
        self.shapes.append(shape)

    def paintEvent(self, event):
        painter = QPainter(self)
        for shape in self.shapes:
            shape.draw(painter)


def main():
    app = QApplication([])
    w = Window()
    b = Ball(30, 30, 55, 20)
    b.velocity.setX(10)
    w.add_shape(b)
    r = Rect(0, 440, 1000000000, 500, 20)
    w.add_shape(r)
    app.exec()


if __name__ == '__main__':
    main()
