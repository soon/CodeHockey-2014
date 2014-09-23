"""
This module provides classes for representing defenceman kicker strategy
"""
from kicker_strategy import KickerStrategy


class DefencemanKickerStrategy(KickerStrategy):
    @property
    def opponent_to_be_attacked(self):
        return self.opponent_defenceman or self.nearest_opponent