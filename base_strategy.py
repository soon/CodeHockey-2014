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
from vector import Vector


__all__ = ['BaseStrategy']


class BaseStrategy:

    def __init__(self, me: Hockeyist, world: World, game: Game, move: Move, info):
        self._me = None
        self._world = None
        self._game = None
        self._move = None
        self._info = None

        self.me = me
        self.world = world
        self.game = game
        self.move = move
        self.info = info

        self._dangerous_puck_speed_vector_length = 15
        self._allowed_opponent_distance_to_our_goal_net = 600
        self._allowed_angle_between_codirectional_vectors = 0.1
        self._opponent_defenceman_distance = 120

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
    def puck_is_free(self):
        return self.puck_owner is None

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

    def unit_is_moving_to_us(self, unit):
        speed_vector = self.get_speed_vector(unit)
        vector_to_us = Vector(self.get_unit_position(unit), self.get_unit_position(self.me))

        return abs(speed_vector.angle_to(vector_to_us)) < self._allowed_angle_between_codirectional_vectors

    @property
    def angle(self):
        return self.me.angle

    @property
    def nearest_teammate(self):
        # The first item is the player itself, so, return the second
        return sorted(self.my_hockeyists, key=self.get_distance_to_unit)[1]

    @property
    def nearest_opponent(self):
        return sorted(self.opponent_hockeyists, key=self.get_distance_to_unit)[1]

    @property
    def angle_to_nearest_teammate(self):
        return self.get_angle_to_unit(self.nearest_teammate)

    @property
    def angle_to_nearest_opponent(self):
        return self.get_angle_to_unit(self.nearest_opponent)

    def get_angle_to_goal_net_center(self, player):
        return self.get_angle_to_unit(self.get_goal_net_center(player))

    @property
    def angle_to_opponent_goal_net_center(self):
        return self.get_angle_to_goal_net_center(self.opponent)

    def can_pass_to(self, teammate):
        return self.get_angle_to_unit(teammate) < self.pass_sector / 2

    def get_pass_angle_to(self, hockeyist):
        absolute_pass_angle = self.get_angle_to_unit(hockeyist)
        relative_pass_angle = absolute_pass_angle - self.pass_angle

        return self.normalize_angle(relative_pass_angle)

    @staticmethod
    def normalize_angle(angle):
        while angle > pi:
            angle -= 2.0 * pi

        while angle < -pi:
            angle += 2.0 * pi

        return angle

    @staticmethod
    def invert_angle(angle):
        return BaseStrategy.normalize_angle(angle + pi)

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
        return [h for h in self.opponent_hockeyists_with_goalie if h.type != HockeyistType.GOALIE]

    @property
    def opponent_hockeyists_with_goalie(self):
        return [h for h in self.hockeyists if not h.teammate]

    @property
    def my_hockeyists(self) -> [Hockeyist]:
        return [h for h in self.my_hockeyists_with_goalie if h.type != HockeyistType.GOALIE]

    @property
    def my_hockeyists_with_goalie(self):
        return [h for h in self.hockeyists if h.teammate]

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
    def goal_net_bottom_corner(self):
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
        return self.swing_at_most(self.max_effective_swing_ticks)

    def swing_at_most(self, max_swing_ticks):
        if self.swing_ticks >= max_swing_ticks:
            return ActionType.STRIKE
        else:
            return ActionType.SWING

    @property
    def take_puck_or_prevent_attack_or_attack_opponent(self):
        if self.own_puck:
            return ActionType.NONE
        elif self.can_influence_puck:
            if self.opponent_team_own_puck or self.puck_is_dangerous:
                return ActionType.STRIKE
            else:
                return ActionType.TAKE_PUCK
        elif self.can_influence_opponent:
            return self.kick_opponent_action
        elif self.last_action == ActionType.SWING:
            return ActionType.CANCEL_STRIKE
        else:
            return ActionType.NONE

    @property
    def influence_opponent_action(self):
        if self.can_influence_opponent:
            return self.kick_opponent_action
        elif self.last_action == ActionType.SWING:
            return ActionType.CANCEL_STRIKE
        else:
            return ActionType.NONE

    def unit_is_ahead(self, unit):
        return abs(self.get_angle_to_unit(unit)) < pi / 2

    def unit_is_behind(self, unit):
        return not self.unit_is_ahead(unit)

    @staticmethod
    def get_speed_vector(unit) -> Vector:
        return Vector(BaseStrategy.get_unit_position(unit),
                      BaseStrategy.get_unit_position(unit) + Point(unit.speed_x, unit.speed_y))

    @staticmethod
    def get_unit_position(unit) -> Point:
        return Point(unit.x, unit.y)

    @property
    def puck_speed_vector(self) -> Vector:
        return self.get_speed_vector(self.puck)

    @staticmethod
    def vector_is_between(v1, v2, v3):
        angle1 = v1.angle_to(v2)
        angle2 = v1.angle_to(v3)

        return (angle1 <= 0 <= angle2 or angle2 <= 0 <= angle1) and abs(angle1) < pi / 2 and abs(angle2) < pi / 2

    @property
    def puck_is_moving(self):
        return self.puck_speed_vector.length > 0

    @property
    def puck_position(self):
        return Point(self.puck.x, self.puck.y)

    def puck_is_moving_to_goal_net(self, player):
        top = Vector(self.puck_position, self.get_goal_net_top_corner(player))
        bottom = Vector(self.puck_position, self.get_goal_net_bottom_corner(player))

        return self.puck_is_free and self.puck_is_moving and self.vector_is_between(self.puck_speed_vector, top, bottom)

    @property
    def puck_is_moving_to_our_goal_net(self):
        return self.puck_is_moving_to_goal_net(self.player)

    @property
    def puck_is_moving_to_opponent_goal_net(self):
        return self.puck_is_moving_to_goal_net(self.opponent)

    @property
    def puck_is_dangerous(self):
        return (self.puck_is_moving_to_our_goal_net and
                self.puck_speed_vector.length > self._dangerous_puck_speed_vector_length)

    @property
    def opponent_is_going_to_attack(self):
        if self.opponent_team_own_puck:
            puck_owner = self.puck_owner

            center = Vector(self.get_unit_position(puck_owner), self.goal_net_center)
            top = Vector(self.get_unit_position(puck_owner), self.goal_net_top_corner)
            bottom = Vector(self.get_unit_position(puck_owner), self.goal_net_bottom_corner)

            return (self.vector_is_between(center, top, bottom) and
                    center.length < self._allowed_opponent_distance_to_our_goal_net)
        else:
            return False

    @property
    def opponent_defenceman(self):
        defenceman = sorted(self.opponent_hockeyists,
                            key=lambda h: h.get_distance_to_unit(self.opponent_goal_net_center))[0]

        if defenceman.get_distance_to_unit(self.opponent_goal_net_center) < self._opponent_defenceman_distance:
            return defenceman
        else:
            return None

    @property
    def opponent_has_defenceman(self):
        return self.opponent_defenceman is not None

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

    @property
    def info(self):
        """
        Allows to share info between instances of strategies
        """
        return self._info

    @info.setter
    def info(self, value):
        self._info = value

    @staticmethod
    def initial_info():
        return {}

    #endregion
