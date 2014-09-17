"""
This module provides class for representing base strategy.
Every strategy should inherit this class.
"""
from math import pi

from model.HockeyistState import HockeyistState
from model.HockeyistType import HockeyistType
from model.Puck import Puck
from model.Player import Player
from model.ActionType import ActionType
from model.Game import Game
from model.Hockeyist import Hockeyist
from model.Move import Move
from model.Unit import Unit
from model.World import World
from iter import first
from point import Point


__all__ = ['BaseStrategy']


class BaseStrategy:

    def __init__(self, me: Hockeyist, world: World, game: Game, move: Move):
        self._me = None
        self._world = None
        self._game = None
        self._move = None

        self.me = me
        self.world = world
        self.game = game
        self.move = move

    #region Utils

    @property
    def distance_to_puck(self) -> float:
        return self.me.get_distance_to_unit(self.world.puck)

    @property
    def our_team_own_puck(self) -> bool:
        owner = self.puck_owner
        return owner is not None and owner.teammate

    @property
    def own_puck(self):
        return self.our_team_own_puck and self.puck_owner.id == self.me.id

    @property
    def opponent_team_own_puck(self):
        return not self.our_team_own_puck and self.puck_owner is not None

    @property
    def puck_owner(self) -> Hockeyist:
        return self.get_hockeyist_by_id(self.world.puck.owner_hockeyist_id)

    def get_hockeyist_by_id(self, hockeyist_id) -> Hockeyist:
        return first(self.world.hockeyists, lambda h: h.id == hockeyist_id)

    @property
    def goal_net_center(self) -> Point:
        return self.get_goal_net_center(self.player)

    @property
    def opponent_goal_net_center(self) -> Point:
        return self.get_goal_net_center(self.opponent)

    @property
    def goal_net_horizontal(self):
        return 460
    
    @property
    def net_back(self):
        return self.player.net_back

    @property
    def net_front(self):
        return self.player.net_front

    @property
    def goal_net_height(self):
        return self.game.goal_net_height

    @property
    def player(self) -> Player:
        return first(self.world.players, lambda p: p.me)

    @property
    def opponent(self) -> Player:
        return first(self.world.players, lambda p: not p.me)

    @staticmethod
    def get_goal_net_center(player: Player) -> Point:
        return Point(player.net_front, (player.net_bottom + player.net_top) / 2)

    @property
    def puck(self) -> Puck:
        return self.world.puck

    @property
    def stick_length(self):
        return self.game.stick_length

    @property
    def stick_sector(self):
        return self.game.stick_sector

    def get_distance_to_unit(self, unit):
        return self.me.get_distance_to_unit(unit)

    def get_distance(self, x, y):
        return self.get_angle_to_unit(Point(x, y))

    def get_angle_to_unit(self, unit):
        return self.me.get_angle_to_unit(unit)

    def get_angle_to(self, x, y):
        return self.me.get_angle_to(x, y)

    @property
    def angle(self):
        return self.me.angle

    @property
    def nearest_teammate(self):
        # The first item is the player itself, so, return the second
        return sorted(self.my_hockeyists, key=self.get_distance_to_unit)[1]

    @property
    def angle_to_nearest_teammate(self):
        return self.get_angle_to_unit(self.nearest_teammate)

    def can_pass_to(self, teammate):
        return self.get_angle_to_unit(teammate) < self.pass_sector / 2

    def get_pass_angle_to(self, hockeyist):
        absolute_pass_angle = self.get_angle_to_unit(hockeyist)
        relative_pass_angle = absolute_pass_angle - self.pass_angle

        while relative_pass_angle > pi:
            relative_pass_angle -= 2.0 * pi

        while relative_pass_angle < -pi:
            relative_pass_angle += 2.0 * pi

        return relative_pass_angle

    @property
    def pass_angle(self):
        return self.move.pass_angle

    @pass_angle.setter
    def pass_angle(self, angle):
        assert isinstance(angle, (int, float))
        self.move.pass_angle = float(angle)

    @property
    def pass_sector(self):
        return self.game.pass_sector

    def get_real_distance_to_unit(self, other: Unit):
        return self.get_distance_to_unit(other) - self.me.radius - other.radius

    def can_influence_by_stick(self, other: Unit) -> bool:
        return (self.get_distance_to_unit(other) < self.stick_length and
                abs(self.get_angle_to_unit(other)) < self.stick_sector / 2)

    @property
    def can_influence_puck(self) -> bool:
        return self.can_influence_by_stick(self.puck)

    @property
    def opponent_hockeyists(self) -> [Hockeyist]:
        return [h for h in self.hockeyists if not h.teammate]

    @property
    def my_hockeyists(self) -> [Hockeyist]:
        return [h for h in self.hockeyists if h.teammate and h.type != HockeyistType.GOALIE]

    @property
    def last_action(self):
        return self.me.last_action

    @property
    def max_effective_swing_ticks(self):
        return self.game.max_effective_swing_ticks
        
    @property
    def swing_ticks(self):
        return self.me.swing_ticks

    @property
    def hockeyists(self) -> [Hockeyist]:
        return self.world.hockeyists

    @property
    def can_influence_opponent(self):
        return any(map(self.can_influence_by_stick, self.opponent_hockeyists))

    @property
    def state(self) -> HockeyistState:
        return self.me.state

    @property
    def angle_to_puck(self):
        return self.get_angle_to_unit(self.puck)

    @property
    def goal_net_top_corner(self):
        return self.get_goal_net_top_corner(self.player)

    @property
    def goal_net_top_corner(self):
        return self.get_goal_net_bottom_corner(self.player)

    @staticmethod
    def get_goal_net_top_corner(player):
        return Point(player.net_front, player.net_top)

    @staticmethod
    def get_goal_net_bottom_corner(player):
        return Point(player.net_front, player.net_bottom)

    @property
    def kick_opponent_action(self):
        return self.swing_as_long_as_needed

    @property
    def swing_as_long_as_needed(self):
        if self.swing_ticks >= self.max_effective_swing_ticks:
            return ActionType.STRIKE
        else:
            return ActionType.SWING

    @property
    def influence_opponent_action(self):
        if self.can_influence_opponent:
            return self.kick_opponent_action
        elif self.last_action == ActionType.SWING:
            return ActionType.CANCEL_STRIKE
        else:
            return ActionType.NONE

    #endregion

    #region Properties

    @property
    def me(self):
        """
        :rtype: Hockeyist
        """
        return self._me

    @me.setter
    def me(self, value):
        assert isinstance(value, Hockeyist)
        self._me = value

    @property
    def world(self):
        """
        :rtype: World
        """
        return self._world

    @world.setter
    def world(self, value):
        assert isinstance(value, World)
        self._world = value

    @property
    def game(self):
        """
        :rtype: Game
        """
        return self._game

    @game.setter
    def game(self, value):
        assert isinstance(value, Game)
        self._game = value

    @property
    def move(self):
        """
        :rtype: Move
        """
        return self._move

    @move.setter
    def move(self, value):
        assert isinstance(value, Move)
        self._move = value

    @property
    def speed_up(self):
        """
        :return: By default returns 0
        """
        return 0

    @property
    def turn(self):
        """
        :return: By default returns 0
        """
        return 0

    @property
    def action(self):
        """
        :return: By default returns ActionType.NONE
        """
        return ActionType.NONE

    #endregion
