"""
This module provides classes for representing forward strategy
"""
from math import copysign

from model.ActionType import ActionType
from base_strategy import BaseStrategy
from point import Point


__all__ = ['ForwardStrategy']


class ForwardStrategy(BaseStrategy):

    def __init__(self, me, world, game, move):
        super().__init__(me, world, game, move)

        self._allowed_distance = 130
        self._allowed_distance_to_strike = 70
        self._allowed_angle = 0.06
        self._max_swing_ticks = 8

    @property
    def speed_up(self):
        if self.own_puck:
            if (self.angle_to_nearest_attack_position < self._allowed_angle or
                    self.distance_to_nearest_attack_position > self._allowed_distance):
                return 1.0
            else:
                return -0.7
        else:
            return 1.0

    @property
    def turn(self):
        if self.our_team_own_puck:
            if self.distance_to_nearest_attack_position < self._allowed_distance:
                return self.angle_to_goal_position
            else:
                return self.angle_to_nearest_attack_position
        else:
            return self.angle_to_puck

    @property
    def action(self):
        if self.own_puck:
            if self.distance_to_nearest_attack_position < self._allowed_distance_to_strike:
                if abs(self.angle_to_goal_position) < self._allowed_angle:
                    if self.swing_ticks >= self._max_swing_ticks:
                        return ActionType.STRIKE
                    else:
                        return ActionType.SWING
        elif self.can_influence_puck:
            return ActionType.TAKE_PUCK
        else:
            return self.influence_opponent_action

        return ActionType.CANCEL_STRIKE

    @staticmethod
    def get_attack_vertical(player):
        return abs(500 - player.net_back)

    @property
    def attack_vertical(self):
        return self.get_attack_vertical(self.opponent)

    @property
    def attack_position(self) -> [Point]:
        return [
            Point(self.attack_vertical, 215.0),
            Point(self.attack_vertical, 685.0)
        ]

    def get_goal_position(self, attack_point: Point) -> Point:
        return Point((self.opponent.net_front + self.opponent.net_back) / 2,
                     copysign(self.goal_net_height / 2,
                              self.goal_net_horizontal - attack_point.y) + self.goal_net_horizontal)

    @property
    def nearest_attack_position(self):
        return sorted(self.attack_position, key=self.get_distance_to_unit)[0]

    @property
    def angle_to_nearest_attack_position(self):
        return self.get_angle_to_unit(self.nearest_attack_position)

    @property
    def angle_to_goal_position(self):
        return self.get_angle_to_unit(self.nearest_goal_position)

    @property
    def distance_to_nearest_attack_position(self):
        return self.get_distance_to_unit(self.nearest_attack_position)

    @property
    def distance_to_nearest_goal_position(self):
        return self.get_distance_to_unit(self.nearest_goal_position)

    @property
    def nearest_goal_position(self):
        return self.get_goal_position(self.nearest_attack_position)
