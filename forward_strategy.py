"""
This module provides classes for representing forward strategy
"""
from enum import Enum
from math import copysign

from model.ActionType import ActionType
from base_strategy import BaseStrategy
from point import Point


__all__ = ['ForwardStrategy']


class StrategyState(Enum):
    undefined = 1
    take_puck = 2
    set_to_attack = 3
    go_to_attack_position = 4
    rotate_to_goal_position = 5
    move_to_goal_position = 6
    ready_to_strike = 7


class ForwardStrategy(BaseStrategy):

    def __init__(self, me, world, game, move, info):
        super().__init__(me, world, game, move, info)

        self._allowed_distance_to_pre_attack_position = 50
        self._allowed_distance_to_goal_position = 400
        self._allowed_distance = 70
        self._allowed_distance_to_strike = 70
        self._allowed_angle = 0.06
        self._max_swing_ticks = 8
        self._allowed_distance_to_opponent = 75

        self.update_state()

    @property
    def speed_up(self):
        return {
            StrategyState.undefined: 1.0,
            StrategyState.take_puck: 1.0,
            StrategyState.set_to_attack: 1.0,
            StrategyState.go_to_attack_position: 1.0,
            StrategyState.rotate_to_goal_position: -0.5,
            StrategyState.move_to_goal_position: 1.0,
            StrategyState.ready_to_strike: 1.0
        }[self.info['state']]

    @property
    def turn(self):
        return {
            StrategyState.undefined: 0.0,
            StrategyState.take_puck: self.angle_to_puck,
            StrategyState.set_to_attack: self.angle_to_nearest_pre_attack_position,
            StrategyState.go_to_attack_position: self.angle_to_nearest_attack_position,
            StrategyState.rotate_to_goal_position: self.angle_to_goal_position,
            StrategyState.move_to_goal_position: self.angle_to_goal_position,
            StrategyState.ready_to_strike: self.angle_to_goal_position
        }[self.info['state']]

    @property
    def action(self):
        return {
            StrategyState.undefined: self.take_puck_or_prevent_attack_or_attack_opponent,
            StrategyState.take_puck: self.take_puck_or_prevent_attack_or_attack_opponent,
            StrategyState.set_to_attack: ActionType.NONE,
            StrategyState.go_to_attack_position: ActionType.NONE,
            StrategyState.rotate_to_goal_position: ActionType.NONE,
            StrategyState.move_to_goal_position: ActionType.NONE,
            StrategyState.ready_to_strike: self.swing_at_most(self._max_swing_ticks)
        }[self.info['state']]

    @staticmethod
    def initial_info():
        return {
            'state': StrategyState.undefined
        }

    @staticmethod
    def get_attack_vertical(player):
        return abs(500 - player.net_back)

    @property
    def attack_vertical(self):
        return self.get_attack_vertical(self.opponent)

    @property
    def attack_positions(self) -> [Point]:
        return [
            Point(self.attack_vertical, 200.0),
            Point(self.attack_vertical, 720.0)
        ]

    @staticmethod
    def get_pre_attack_vertical(player):
        return abs(700 - player.net_back)

    @property
    def pre_attack_vertical(self):
        return self.get_pre_attack_vertical(self.opponent)

    @property
    def pre_attack_positions(self):
        return [Point(self.pre_attack_vertical, p.y) for p in self.attack_positions]

    def get_goal_position(self, attack_point: Point) -> Point:
        return Point((self.opponent.net_front + self.opponent.net_back) / 2,
                     copysign(self.goal_net_height / 2,
                              self.goal_net_horizontal - attack_point.y) + self.goal_net_horizontal)

    def update_state(self):
        new_state = self.get_next_state(self.state)

        while self.state != new_state:
            self.state = new_state
            new_state = self.get_next_state(self.state)

    def get_next_state(self, state):
        if self.our_team_own_puck:
            if state in (StrategyState.undefined, StrategyState.take_puck):
                state = StrategyState.set_to_attack

            elif (state == StrategyState.set_to_attack and
                    self.distance_to_nearest_pre_attack_position < self._allowed_distance_to_pre_attack_position):
                state = StrategyState.go_to_attack_position

            elif (state == StrategyState.go_to_attack_position and
                    self.distance_to_nearest_attack_position < self._allowed_distance):
                state = StrategyState.rotate_to_goal_position

            elif (state == StrategyState.rotate_to_goal_position and
                    abs(self.angle_to_goal_position) < self._allowed_angle):
                state = StrategyState.move_to_goal_position

            elif state == StrategyState.move_to_goal_position and self.time_to_strike:
                state = StrategyState.ready_to_strike
        else:
            state = StrategyState.take_puck

        return state

    @property
    def time_to_strike(self):
        return (self.distance_to_nearest_goal_position < self._allowed_distance_to_goal_position or
                self.opponent_is_going_to_prevent_attack or
                self.opponent_is_nearby or
                (self.opponent_has_defenceman and
                    self.get_distance_to_unit(self.opponent_defenceman) < self._allowed_distance_to_opponent))

    @property
    def state(self):
        return self.info['state']

    @state.setter
    def state(self, value):
        self.info['state'] = value

    @property
    def opponent_is_going_to_prevent_attack(self):
        return any(self.unit_is_ahead(h) and self.unit_is_moving_to_us(h) for h in self.opponent_hockeyists)

    @property
    def opponent_is_nearby(self):
        return any(self.get_distance_to_unit(h) < self._allowed_distance_to_opponent for h in self.opponent_hockeyists)

    @property
    def nearest_pre_attack_position(self):
        return sorted(self.pre_attack_positions, key=self.get_distance_to_unit)[0]

    @property
    def angle_to_nearest_pre_attack_position(self):
        return self.get_angle_to_unit(self.nearest_pre_attack_position)

    @property
    def nearest_attack_position(self):
        return sorted(self.attack_positions, key=self.get_distance_to_unit)[0]

    @property
    def angle_to_nearest_attack_position(self):
        return self.get_angle_to_unit(self.nearest_attack_position)

    @property
    def angle_to_goal_position(self):
        return self.get_angle_to_unit(self.nearest_goal_position)

    @property
    def distance_to_nearest_pre_attack_position(self):
        return self.get_distance_to_unit(self.nearest_pre_attack_position)

    @property
    def distance_to_nearest_attack_position(self):
        return self.get_distance_to_unit(self.nearest_attack_position)

    @property
    def distance_to_nearest_goal_position(self):
        return self.get_distance_to_unit(self.nearest_goal_position)

    @property
    def nearest_goal_position(self):
        return self.get_goal_position(self.nearest_attack_position)
