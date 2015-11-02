"""
This module provides classes for representing 2x2 strategies factory
"""
from base_strategy import BaseStrategy
from base_strategy_factory import BaseStrategyFactory
from defence_strategy import DefenceStrategy
from defenceman_kicker_strategy import DefencemanKickerStrategy
from forward_strategy import ForwardStrategy
from no_goalies_strategy import NoGoaliesStrategy

__all__ = ['Strategy2x2Factory']


class Strategy2x2Factory(BaseStrategyFactory):
    @staticmethod
    def is_forward(strategy: BaseStrategy):
        return strategy.own_puck or sorted(strategy.my_hockeyists,
                                           key=lambda h: h.get_distance_to_unit(strategy.puck))[0].id == strategy.me.id

    def create_strategy(self, me, world, game, move) -> BaseStrategy:
        strategy = self.create_base_strategy(me, world, game, move)

        if strategy.no_goalies():
            strategy = NoGoaliesStrategy
        elif strategy.my_score == strategy.opponent_score:
            if strategy.opponent_team_own_puck:
                strategy = self.last_strategies[me.id]

                if (strategy == DefencemanKickerStrategy or
                        all(s == ForwardStrategy for s in self.last_strategies.values())):
                    strategy = DefenceStrategy
            else:
                strategy = ForwardStrategy if self.is_forward(strategy) else DefenceStrategy
        else:
            if self.is_forward(strategy):
                strategy = ForwardStrategy
            else:
                strategy = DefenceStrategy

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
