"""
This module provides classes for sharing info between strategies
"""


class StrategiesSharedInfo:
    _instance = None
    _info = {}
    _last_strategy = {}

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls, *args)
        return cls._instance

    @property
    def info(self):
        return self._info

    @info.setter
    def info(self, value):
        self._info = value

    @property
    def last_strategy(self):
        return self._last_strategy

    @last_strategy.setter
    def last_strategy(self, value):
        self._last_strategy = value