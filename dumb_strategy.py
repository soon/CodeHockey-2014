from base_strategy import BaseStrategy

from point import Point


__all__ = ['DumbStrategy']


class DumbStrategy(BaseStrategy):
    """
    Moves to left upper corner and does nothing
    """

    @property
    def turn(self):
        return self.get_angle_to_unit(Point(0, 0))

    @property
    def speed_up(self):
        return 1.0
