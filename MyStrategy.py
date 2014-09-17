from model.Game import Game
from model.HockeyistType import HockeyistType
from model.Move import Move
from model.Hockeyist import Hockeyist
from model.World import World
from strategies.forward_strategy import ForwardStrategy
from strategies.base_strategy import BaseStrategy
from strategies.defence_strategy import DefenceStrategy
from strategies.no_goalies_strategy import NoGoaliesStrategy


class MyStrategy:

    @staticmethod
    def no_goalies(world):
        return not any(h.type == HockeyistType.GOALIE for h in world.hockeyists)

    @staticmethod
    def create_strategy(me, world, game, move) -> BaseStrategy:
        if MyStrategy.no_goalies(world):
            strategy = NoGoaliesStrategy
        else:
            strategy = [ForwardStrategy,
                        DefenceStrategy][me.teammate_index]

        return strategy(me, world, game, move)

    def move(self, me: Hockeyist, world: World, game: Game, move: Move):
        strategy = self.create_strategy(me, world, game, move)

        move.action = strategy.action
        move.speed_up = strategy.speed_up
        move.turn = strategy.turn