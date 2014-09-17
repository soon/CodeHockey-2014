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

    @staticmethod
    def no_goalies(world):
        return not any(h.type == HockeyistType.GOALIE for h in world.hockeyists)

    @staticmethod
    def is_defender(me, hockeyists):
        return me.id == min(h.id for h in hockeyists)

    @staticmethod
    def create_strategy(me, world, game, move) -> BaseStrategy:
        strategy = BaseStrategy(me, world, game, move)

        if MyStrategy.no_goalies(world):
            strategy = NoGoaliesStrategy
        elif MyStrategy.is_defender(me, strategy.my_hockeyists):
            strategy = DefenceStrategy
        else:
            strategy = ForwardStrategy

        return strategy(me, world, game, move)

    def move(self, me: Hockeyist, world: World, game: Game, move: Move):
        strategy = self.create_strategy(me, world, game, move)

        move.action = strategy.action
        move.speed_up = strategy.speed_up
        move.turn = strategy.turn
