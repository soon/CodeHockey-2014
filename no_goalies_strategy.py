"""
This module provides classes for representing strategy in case if there is no goalies
"""
from base_strategy import BaseStrategy
from defence_strategy import DefenceStrategy
from simple_striker_strategy import SimpleStrikerStrategy


__all__ = ['NoGoaliesStrategy']


class NoGoaliesStrategy(BaseStrategy):

    def __init__(self, me, world, game, move):
        super().__init__(me, world, game, move)

        strategy = SimpleStrikerStrategy if self.our_team_own_puck else DefenceStrategy

        self.strategy = strategy(me, world, game, move)

    @property
    def speed_up(self):
        return self.strategy.speed_up

    @property
    def turn(self):
        return self.strategy.turn

    @property
    def action(self):
        return self.strategy.action
