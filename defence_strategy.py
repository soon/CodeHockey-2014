"""
This module provides classes for representing defender strategy
"""
from model.ActionType import ActionType

from base_strategy import BaseStrategy

from point import Point
from vector import Vector


__all__ = ['DefenceStrategy']


class DefenceStrategy(BaseStrategy):

    def __init__(self, me, world, game, move, info):
        super().__init__(me, world, game, move, info)

        self._allowed_distance_to_point = 50
        self._max_distance = 50
        self._coefficient = 0.7
        self._max_opponent_distance = self._max_distance / self._coefficient

    @property
    def speed_up(self):
        return self.optimal_distance / 170

    @property
    def turn(self):
        if self.own_puck:
            return self.angle_to_nearest_teammate
        else:
            optimal_position = self.optimal_position
            if self.get_distance_to_unit(optimal_position) > self._allowed_distance_to_point:
                return self.get_angle_to_unit(optimal_position)
            else:
                return self.angle_to_puck

    @property
    def action(self):
        if self.can_influence_puck:
            if self.own_puck:
                self.pass_angle = self.get_pass_angle_to(self.nearest_teammate)

                if self.can_pass_to(self.nearest_teammate):
                    return ActionType.PASS
                else:
                    return ActionType.NONE
            else:
                return ActionType.TAKE_PUCK
        else:
            return self.influence_opponent_action

    @property
    def vector_from_goal_net_to_puck(self) -> Vector:
        return Vector(self.goal_net_center, self.puck)

    @property
    def optimal_position(self) -> Point:
        v = self.vector_from_goal_net_to_puck
        v.length = self.optimal_distance
        return v.end

    @property
    def optimal_distance(self):
        return max(self._max_distance, int(self.distance_to_puck * self._coefficient))

    @property
    def distance_from_net_to_player(self):
        return self.get_distance_to_unit(self.goal_net_center)