from model.Game import Game
from model.Move import Move
from model.Hockeyist import Hockeyist
from model.World import World
from strategies.base_strategy import BaseStrategy
from strategies.defence_strategy import DefenceStrategy
from strategies.dumb_strategy import DumbStrategy


class MyStrategy:

    @staticmethod
    def create_strategy(me, world, game, move) -> BaseStrategy:
        return [DumbStrategy,
                DefenceStrategy][me.teammate_index](me, world, game, move)

    def move(self, me: Hockeyist, world: World, game: Game, move: Move):
        strategy = self.create_strategy(me, world, game, move)

        move.action = strategy.action
        move.speed_up = strategy.speed_up
        move.turn = strategy.turn
