"""
This module provides classes for representing vector
"""
from math import hypot

from point import Point


class Vector:
    def __init__(self, start: Point, end: Point):
        self.start = start
        self.end = end

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
