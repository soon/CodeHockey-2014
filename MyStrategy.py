from base_strategy_factory import BaseStrategyFactory
from model.Game import Game
from model.HockeyistType import HockeyistType
from model.Move import Move
from model.Hockeyist import Hockeyist
from model.World import World
from base_strategy import BaseStrategy
from strategy_2x2_factory import Strategy2x2Factory
from strategy_2x3_factory import Strategy2x3Factory
from strategy_2x6_factory import Strategy2x6Factory


class MyStrategy:
    @staticmethod
    def no_goalies(world):
        return not any(h.type == HockeyistType.GOALIE for h in world.hockeyists)

    @staticmethod
    def is_forward(strategy: BaseStrategy):
        return strategy.own_puck or sorted(strategy.my_hockeyists,
                                           key=lambda h: h.get_distance_to_unit(strategy.puck))[0].id == strategy.me.id

    def create_factory(self, me, world, game, move) -> BaseStrategyFactory:
        base_strategy = BaseStrategy(me, world, game, move)
        factory = {
            2: Strategy2x2Factory,
            3: Strategy2x3Factory,
            6: Strategy2x6Factory
        }[len(base_strategy.my_hockeyists)]

        return factory()

    def create_strategy(self, factory, me, world, game, move) -> BaseStrategy:
        return factory.create_strategy(me, world, game, move)

    def move(self, me: Hockeyist, world: World, game: Game, move: Move):
        factory = self.create_factory(me, world, game, move)
        strategy = self.create_strategy(factory, me, world, game, move)

        move.action = strategy.action
        move.speed_up = strategy.speed_up
        move.turn = strategy.turn

        factory.info[type(strategy)] = strategy.info