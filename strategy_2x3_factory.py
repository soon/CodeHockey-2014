"""
This module provides classes for representing 2x3 strategies factory
"""
from base_strategy import BaseStrategy
from base_strategy_factory import BaseStrategyFactory
from defence_strategy import DefenceStrategy
from defenceman_kicker_strategy import DefencemanKickerStrategy
from forward_strategy import ForwardStrategy
from model.HockeyistType import HockeyistType
from no_goalies_strategy import NoGoaliesStrategy

__all__ = ['Strategy2x2Factory']


class Strategy2x3Factory(BaseStrategyFactory):
    def create_strategy(self, me, world, game, move) -> BaseStrategy:
        strategy = self.create_base_strategy(me, world, game, move)

        if strategy.no_goalies():
            strategy = NoGoaliesStrategy
        else:
            if strategy.our_team_own_puck:
                strategy = {
                    HockeyistType.VERSATILE: DefencemanKickerStrategy,
                    HockeyistType.FORWARD: ForwardStrategy,
                    HockeyistType.DEFENCEMAN: DefenceStrategy
                }[strategy.me.type]
            else:
                strategy = {
                    HockeyistType.VERSATILE: DefenceStrategy,
                    HockeyistType.FORWARD: ForwardStrategy,
                    HockeyistType.DEFENCEMAN: DefenceStrategy
                }[strategy.me.type]

        self.last_strategies[me.id] = strategy

        return strategy(me, world, game, move, self.info[strategy])

    @property
    def strategies(self):
        return [
            BaseStrategy,
            DefenceStrategy,
            ForwardStrategy,
            NoGoaliesStrategy,
            DefencemanKickerStrategy
        ]