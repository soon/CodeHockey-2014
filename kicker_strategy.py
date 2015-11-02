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
        return self.get_angle_to_unit(self.future_opponent_position)

    @property
    def action(self):
        if self.can_influence_by_stick(self.future_opponent_position):
            return self.kick_opponent_action
        else:
            return ActionType.CANCEL_STRIKE

    @property
    def opponent_to_be_attacked(self):
        return self.nearest_opponent

    @property
    def future_opponent_position(self):
        return self.optimal_position_to_interact_with(self.opponent_to_be_attacked)