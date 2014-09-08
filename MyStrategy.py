from math import *
from model.HockeyistState import HockeyistState
from model.ActionType import ActionType
from model.Game import Game
from model.HockeyistType import HockeyistType
from model.Move import Move
from model.Hockeyist import Hockeyist
from model.World import World


class MyStrategy:
    
    STRIKE_ANGLE = 5 * pi / 180.0

    @staticmethod
    def get_nearest_opponent(x: float, y: float, world: World):
        nearest_opponent = None
        nearest_opponent_range = 0.0

        for hockeyist in world.hockeyists:
            if (hockeyist.teammate or hockeyist.type == HockeyistType.GOALIE or
                    hockeyist.state in [HockeyistState.KNOCKED_DOWN, HockeyistState.RESTING]):
                continue

            opponent_range = hypot(x - hockeyist.x, y - hockeyist.y)

            if nearest_opponent is None or opponent_range < nearest_opponent_range:
                nearest_opponent = hockeyist
                nearest_opponent_range = opponent_range

        return nearest_opponent

    def move(self, me: Hockeyist, world: World, game: Game, move: Move):
        if me.state == HockeyistState.SWINGING:
            move.action = ActionType.STRIKE
            return

        if world.puck.owner_player_id == me.player_id:
            if world.puck.owner_hockeyist_id == me.id:
                opponent_player = world.get_opponent_player()

                net_x = 0.5 * (opponent_player.net_back + opponent_player.net_front)
                net_y = 0.7 * (opponent_player.net_bottom + opponent_player.net_top)
                net_y += copysign(0.5 * game.goal_net_height, me.y - net_y)

                angle_to_net = me.get_angle_to(net_x, net_y)
                
                move.turn = angle_to_net

                if abs(angle_to_net) < MyStrategy.STRIKE_ANGLE:
                    move.action = ActionType.SWING
                
            else:
                nearest_opponent = self.get_nearest_opponent(me.x, me.y, world)
                if nearest_opponent is not None:
                    if me.get_distance_to_unit(nearest_opponent) > game.stick_length:
                        move.speed_up = 1
                    elif abs(me.get_angle_to_unit(nearest_opponent)) < 0.5 * game.stick_sector:
                        move.action = ActionType.STRIKE

                    move.turn = me.get_angle_to_unit(nearest_opponent)

        else:
            move.speed_up = 1
            move.turn = me.get_angle_to_unit(world.puck)
            move.action = ActionType.TAKE_PUCK