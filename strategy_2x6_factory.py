"""
This module provides classes for representing 2x3 strategies factory
"""
from base_strategy import BaseStrategy
from base_strategy_factory import BaseStrategyFactory
from forward_strategy import ForwardStrategy

__all__ = ['Strategy2x2Factory']


class Strategy2x6Factory(BaseStrategyFactory):
    def create_strategy(self, me, world, game, move) -> BaseStrategy:
        return ForwardStrategy(me, world, game, move, self.info[ForwardStrategy])

    @property
    def strategies(self):
        return [
            ForwardStrategy
        ]
