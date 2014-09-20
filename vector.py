"""
This module provides classes for representing vector
"""
from math import hypot, atan2, pi

from point import Point


class Vector:
    def __init__(self, a, b):

        if isinstance(a, (int, float)) and isinstance(b, (int, float)):
            self.start = Point(0, 0)
            self.end = Point(a, b)
        else:
            self.start = a
            self.end = b

    def __repr__(self):
        return 'Vector({0} -> {1})'.format(self.start, self.end)

    @property
    def dx(self):
        return self.end.x - self.start.x

    @property
    def dy(self):
        return self.end.y - self.start.y

    @property
    def delta(self):
        return Point(self.dx, self.dy)

    @property
    def length(self):
        return hypot(self.dx, self.dy)

    @length.setter
    def length(self, value):
        if self.length != 0:
            k = value / self.length

            delta = self.delta * k

            self.end = self.start + delta

    def angle_to(self, v):
        angle = atan2(v.dy, v.dx) - atan2(self.dy, self.dx)

        while angle > pi:
            angle -= 2.0 * pi

        while angle < -pi:
            angle += 2.0 * pi

        return angle