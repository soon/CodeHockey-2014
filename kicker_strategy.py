"""
This module provides classes for representing kicker strategy
"""
from base_strategy import BaseStrategy
from model.ActionType import ActionType


class KickerStrategy(BaseStrategy):
    @property
    def speed_up(self):
        return 1.0

    @property
    def turn(self):
        return self.get_angle_to_unit(self.opponent_to_be_attacked)

    @property
    def action(self):
        if self.can_influence_by_stick(self.opponent_to_be_attacked):
            return self.kick_opponent_action
        else:
            return ActionType.NONE

    @property
    def opponent_to_be_attacked(self):
        return self.nearest_opponent