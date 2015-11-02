"""
This module provides classes for representing time wasting strategy
"""
from enum import Enum
from base_strategy import BaseStrategy
from model.ActionType import ActionType
from point import Point


class StrategyState(Enum):
    take_puck = 1
    move_to_start_point = 2
    waste_time = 3


class TimeWastingStrategy(BaseStrategy):
    def __init__(self, me, world, game, move, info):
        super().__init__(me, world, game, move, info)

        self._allowed_distance_to_start_point = 50

        self.update_state()
        # print(self.angle_to_start_point)

    @property
    def speed_up(self):
        return 1.0

    @property
    def action(self):
        if self.state == StrategyState.take_puck:
            return self.take_puck_or_prevent_attack_or_attack_opponent
        else:
            return ActionType.NONE

    @property
    def turn(self):
        return {
            StrategyState.take_puck: self.angle_to_puck,
            StrategyState.move_to_start_point: self.angle_to_start_point,
            StrategyState.waste_time: 0.02
        }[self.state]

    def update_state(self):
        new_state = self.get_next_state(self.state)

        while self.state != new_state:
            self.state = new_state
            new_state = self.get_next_state(self.state)

    def get_next_state(self, state):
        if not self.own_puck:
            state = StrategyState.take_puck

        if state == StrategyState.take_puck and self.own_puck:
            state = StrategyState.move_to_start_point
        elif (state == StrategyState.move_to_start_point and
                self.distance_to_start_point < self._allowed_distance_to_start_point):
            state = StrategyState.waste_time

        return state

    @property
    def distance_to_start_point(self):
        return self.get_distance_to_unit(self.start_point)

    @property
    def angle_to_start_point(self):
        return self.get_angle_to_unit(self.start_point)

    @property
    def start_point(self):
        return Point(600, 200)

    @staticmethod
    def initial_info():
        return {
            'state': StrategyState.take_puck
        }

    @property
    def state(self):
        return self.info['state']

    @state.setter
    def state(self, value):
        self.info['state'] = value
