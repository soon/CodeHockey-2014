"""
This module provides classes for representing simply striker strategy
"""
from model.ActionType import ActionType
from strategies.base_strategy import BaseStrategy


class SimpleStrikerStrategy(BaseStrategy):

    def __init__(self, me, world, game, move):
        super().__init__(me, world, game, move)

        self._allowed_angle = 0.07

    @property
    def turn(self):
        return self.get_angle_to_unit(self.opponent_goal_net_center)

    @property
    def action(self):
        if self.get_angle_to_unit(self.opponent_goal_net_center) < self._allowed_angle:
            return ActionType.STRIKE
        else:
            return ActionType.NONE


