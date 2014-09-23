"""
This module provides classes for representing simply striker strategy
"""
from enum import Enum
from model.ActionType import ActionType
from base_strategy import BaseStrategy


class StrategyState(Enum):
    kick_all_opponents = 1
    take_puck = 2
    turn_to_opponent_goal_net = 3
    attack = 4


class SimpleStrikerStrategy(BaseStrategy):

    def __init__(self, me, world, game, move, info):
        super().__init__(me, world, game, move, info)

        self._allowed_angle = 0.3

        self.update_state()

    @property
    def speed_up(self):
        return {
            StrategyState.kick_all_opponents: 1.0,
            StrategyState.take_puck: 1.0,
            StrategyState.turn_to_opponent_goal_net: 0.0,
            StrategyState.attack: 0.0
        }[self.state]

    @property
    def turn(self):
        return {
            StrategyState.kick_all_opponents: self.angle_to_nearest_opponent,
            StrategyState.take_puck: self.angle_to_puck,
            StrategyState.turn_to_opponent_goal_net: self.angle_to_opponent_goal_net_center,
            StrategyState.attack: self.angle_to_opponent_goal_net_center
        }[self.state]

    @property
    def action(self):
        return {
            StrategyState.kick_all_opponents: self.take_puck_or_prevent_attack_or_attack_opponent,
            StrategyState.take_puck: self.take_puck_or_prevent_attack_or_attack_opponent,
            StrategyState.turn_to_opponent_goal_net: ActionType.NONE,
            StrategyState.attack: ActionType.STRIKE
        }[self.state]

    @staticmethod
    def initial_info():
        return {
            'state': StrategyState.kick_all_opponents
        }

    @property
    def state(self):
        return self.info['state']

    @state.setter
    def state(self, value):
        self.info['state'] = value

    def update_state(self):
        new_state = self.get_next_state(self.state)

        while self.state != new_state:
            self.state = new_state
            new_state = self.get_next_state(self.state)

    def get_next_state(self, state):
        if not self.our_team_own_puck:
            state = StrategyState.take_puck
        elif self.own_puck:
            state = StrategyState.turn_to_opponent_goal_net
        else:
            state = StrategyState.kick_all_opponents

        if state == StrategyState.take_puck and self.own_puck:
           state = StrategyState.turn_to_opponent_goal_net

        elif (state == StrategyState.turn_to_opponent_goal_net and
                      abs(self.get_angle_to_unit(self.opponent_goal_net_center)) < self._allowed_angle):
            state = StrategyState.attack

        return state