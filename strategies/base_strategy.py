"""
This module provides class for representing base strategy.
Every strategy should inherit this class.
"""
from model.ActionType import ActionType
from model.Game import Game
from model.Hockeyist import Hockeyist
from model.Move import Move
from model.World import World


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
