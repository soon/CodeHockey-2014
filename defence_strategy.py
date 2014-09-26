"""
This module provides classes for representing defender strategy
"""
from enum import Enum
from model.ActionType import ActionType

from base_strategy import BaseStrategy

from point import Point
from vector import Vector


__all__ = ['DefenceStrategy']


class StrategyState(Enum):
    undefined = 1
    move_to_defence_point = 2
    normalize_speed = 3
    wait_for_attack = 4
    opponent_is_going_to_attack = 5
    the_puck_is_moving_to_our_goal_net = 6
    prevent_attack = 7


class DefenceStrategy(BaseStrategy):

    def __init__(self, me, world, game, move, info):
        super().__init__(me, world, game, move, info)

        self._allowed_distance_to_defence_point = 40
        self._allowed_distance_to_move_backward = 300

        self.update_state()

    @property
    def speed_up(self):
        return {
            StrategyState.undefined: 0.0,
            StrategyState.move_to_defence_point: self.speed_up_to_defence_point,
            StrategyState.normalize_speed: 0.0,
            StrategyState.wait_for_attack: 0.0,
            StrategyState.opponent_is_going_to_attack: 1.0,
            StrategyState.the_puck_is_moving_to_our_goal_net: 0.0,
            StrategyState.prevent_attack: 0.0
        }[self.state]

    @property
    def turn(self):
        return {
            StrategyState.undefined: 0.0,
            StrategyState.move_to_defence_point: self.angle_to_defence_point,
            StrategyState.normalize_speed: 0.0,
            StrategyState.wait_for_attack: self.angle_to_puck,
            StrategyState.opponent_is_going_to_attack: self.get_angle_to_unit(self.optimal_position_to_puck),
            StrategyState.the_puck_is_moving_to_our_goal_net: self.angle_to_puck,
            StrategyState.prevent_attack: self.angle_to_puck
        }[self.state]

    @property
    def action(self):
        return {
            StrategyState.undefined: ActionType.NONE,
            StrategyState.move_to_defence_point: self.take_puck_or_prevent_attack_or_attack_opponent,
            StrategyState.normalize_speed: self.take_puck_or_prevent_attack_or_attack_opponent,
            StrategyState.wait_for_attack: self.take_puck_or_prevent_attack_or_attack_opponent,
            StrategyState.opponent_is_going_to_attack: self.take_puck_or_prevent_attack_or_attack_opponent,
            StrategyState.the_puck_is_moving_to_our_goal_net: ActionType.NONE,
            StrategyState.prevent_attack: ActionType.STRIKE
        }[self.state]

    def update_state(self):
        new_state = self.get_next_state(self.state)

        while self.state != new_state:
            self.state = new_state
            new_state = self.get_next_state(self.state)

    def get_next_state(self, state):
        if self.distance_to_defence_point > self._allowed_distance_to_defence_point:
            if self.state in (StrategyState.undefined,
                              StrategyState.move_to_defence_point,
                              StrategyState.normalize_speed,
                              StrategyState.wait_for_attack) and not self.opponent_is_going_to_attack:
                return StrategyState.move_to_defence_point

        if state == StrategyState.undefined:
            return StrategyState.move_to_defence_point

        elif (state == StrategyState.move_to_defence_point and
                self.distance_to_defence_point < self._allowed_distance_to_defence_point):
            return StrategyState.normalize_speed

        elif state == StrategyState.normalize_speed:
            return StrategyState.wait_for_attack

        elif state == StrategyState.wait_for_attack:
            if self.opponent_is_going_to_attack:
                return StrategyState.opponent_is_going_to_attack
            elif self.puck_is_moving_to_our_goal_net:
                return StrategyState.the_puck_is_moving_to_our_goal_net

        elif state == StrategyState.opponent_is_going_to_attack:
            if self.puck_is_moving_to_our_goal_net:
                return StrategyState.the_puck_is_moving_to_our_goal_net
            elif not self.opponent_is_going_to_attack:
                return StrategyState.move_to_defence_point

        elif state == StrategyState.the_puck_is_moving_to_our_goal_net:
            if not self.puck_is_moving_to_our_goal_net:
                return StrategyState.move_to_defence_point
            if self.can_influence_puck:
                return StrategyState.prevent_attack

        elif state == StrategyState.prevent_attack and not self.puck_is_moving_to_our_goal_net:
            return StrategyState.move_to_defence_point

        return state

    @staticmethod
    def get_defence_vertical(player):
        return abs(140 - player.net_back)

    @property
    def defence_vertical(self):
        return self.get_defence_vertical(self.player)

    @property
    def defence_point(self):
        return Point(self.defence_vertical, self.goal_net_horizontal)
    
    @property
    def distance_to_defence_point(self):
        return self.get_distance_to_unit(self.defence_point)

    @property
    def speed_up_to_defence_point(self):
        speed_up = (self.distance_to_defence_point / 20)**0.5

        if self.should_move_backward(self.defence_point):
            speed_up = -speed_up

        return speed_up

    def should_move_backward(self, position):
        return (self.unit_is_behind(position) and
                self.get_distance_to_unit(position) < self._allowed_distance_to_move_backward)

    @property
    def angle_to_defence_point(self):
        angle = self.get_angle_to_unit(self.defence_point)
        
        if self.should_move_backward(self.defence_point):
            angle = self.invert_angle(angle)
            
        return angle
    
    @property
    def vector_from_goal_net_to_puck(self) -> Vector:
        return Vector(self.goal_net_center, self.puck)

    @property
    def distance_from_net_to_player(self):
        return self.get_distance_to_unit(self.goal_net_center)

    @staticmethod
    def initial_info():
        return {
            'state': StrategyState.undefined
        }

    @property
    def state(self):
        return self.info['state']

    @state.setter
    def state(self, value):
        self.info['state'] = value
