from model.Game import Game
from model.HockeyistType import HockeyistType
from model.Move import Move
from model.Hockeyist import Hockeyist
from model.World import World
from forward_strategy import ForwardStrategy
from base_strategy import BaseStrategy
from defence_strategy import DefenceStrategy
from no_goalies_strategy import NoGoaliesStrategy


class MyStrategy:

    def __init__(self):
        self._strategies_info = None

        self.strategies_info = {strategy: strategy.initial_info for strategy in self.strategies}

    @staticmethod
    def no_goalies(world):
        return not any(h.type == HockeyistType.GOALIE for h in world.hockeyists)

    @staticmethod
    def is_defender(me, hockeyists):
        return me.id == min(h.id for h in hockeyists)

    def create_strategy(self, me, world, game, move) -> BaseStrategy:
        strategy = BaseStrategy(me, world, game, move, self.strategies_info[BaseStrategy])

        if MyStrategy.no_goalies(world):
            strategy = NoGoaliesStrategy
        elif MyStrategy.is_defender(me, strategy.my_hockeyists):
            strategy = DefenceStrategy
        else:
            strategy = ForwardStrategy

        return strategy(me, world, game, move, self.strategies_info[strategy])

    def move(self, me: Hockeyist, world: World, game: Game, move: Move):
        strategy = self.create_strategy(me, world, game, move)

        move.action = strategy.action
        move.speed_up = strategy.speed_up
        move.turn = strategy.turn

    @property
    def strategies(self):
        return [
            BaseStrategy,
            DefenceStrategy,
            ForwardStrategy,
            NoGoaliesStrategy
        ]

    @property
    def strategies_info(self):
        return self._strategies_info

    @strategies_info.setter
    def strategies_info(self, value):
        self._strategies_info = value
