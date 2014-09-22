"""
This module provides classes for representing strategy in case if there is no goalies
"""
from base_strategy import BaseStrategy
from defence_strategy import DefenceStrategy
from simple_striker_strategy import SimpleStrikerStrategy


__all__ = ['NoGoaliesStrategy']


class NoGoaliesStrategy(BaseStrategy):

    def __init__(self, me, world, game, move, info):
        super().__init__(me, world, game, move, info)

        strategy = DefenceStrategy if self.opponent_team_own_puck else SimpleStrikerStrategy

        self.strategy = strategy(me, world, game, move, info[strategy])

    @staticmethod
    def initial_info():
        return {
            SimpleStrikerStrategy: SimpleStrikerStrategy.initial_info(),
            DefenceStrategy: DefenceStrategy.initial_info()
        }

    @property
    def info(self):
        self._info[type(self.strategy)] = self.strategy.info

        return self._info

    @info.setter
    def info(self, value):
        if len(value) == 2 and SimpleStrikerStrategy in value and DefenceStrategy in value:
            self._info = value
        else:
            super().info[type(self.strategy)] = value

    @property
    def speed_up(self):
        return self.strategy.speed_up

    @property
    def turn(self):
        return self.strategy.turn

    @property
    def action(self):
        return self.strategy.action
