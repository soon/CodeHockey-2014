"""
This module provides methods for work with iterables
"""


def first(iterable, predicate=None, default=None):
    if predicate is None:
        predicate = lambda _: True

    return next(filter(predicate, iterable), default)