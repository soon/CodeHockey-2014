"""
This module provides classes for representing point
"""


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __mul__(self, other):
        return Point(self.x * other, self.y * other)

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return self + -other

    def __neg__(self):
        return Point(-self.x, -self.y)

    def __repr__(self):
        return 'Point({0}, {1})'.format(self.x, self.y)