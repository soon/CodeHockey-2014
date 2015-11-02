"""
This module provides classes for representing base strategy factory pattern
"""
from base_strategy import BaseStrategy
from strategies_shared_info import StrategiesSharedInfo

__all__ = ['BaseStrategyFactory']


class BaseStrategyFactory:
    _instance = None

    def __init__(self):
        self._last_strategies = None
        self._strategies_info = StrategiesSharedInfo()

        self.last_strategies = {}
        self.info = self.info or {strategy: strategy.initial_info() for strategy in self.strategies}

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls, *args)
        return cls._instance

    def create_strategy(self, me, world, game, move):
        pass

    def create_base_strategy(self, me, world, game, move):
        return BaseStrategy(me, world, game, move, self.info[BaseStrategy])

    @property
    def strategies(self):
        return []

    @property
    def last_strategies(self):
        return self._last_strategies

    @last_strategies.setter
    def last_strategies(self, value):
        self._last_strategies = value

    @property
    def info(self):
        return self._strategies_info.info

    @info.setter
    def info(self, value):
        self._strategies_info.info = value