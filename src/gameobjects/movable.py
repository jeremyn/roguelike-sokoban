# Copyright 2016, Jeremy Nation <jeremy@jeremynation.me>
# Released under the GPLv3. See included LICENSE file.
from .. import action


_MOVE_TEST = {
    action.UP: {'axis': 'y', 'change': -1},
    action.DOWN: {'axis': 'y', 'change': 1},
    action.LEFT: {'axis': 'x', 'change': -1},
    action.RIGHT: {'axis': 'x', 'change': 1},
}
_DRY_RUN = 'dry run'
_DO_MOVE = 'do move'


class _Movable(object):

    def __init__(self, start_y, start_x, level_sym):
        self.curr_y = start_y
        self.curr_x = start_x
        self.level_sym = level_sym
        self.walkable = [self.level_sym['Floor']]
        self.pushable = self.walkable[:]
        self.pushable.append(self.level_sym['Pit'])
        try:
            self.symbol = self.level_sym[self.__class__.__name__]
        except KeyError:
            raise Exception(
                "Unexpected _Movable derived class: %s" %
                self.__class__.__name__
            )

    def move(self, move_dir, univ, mode=None):
        axis = _MOVE_TEST[move_dir]['axis']
        change = _MOVE_TEST[move_dir]['change']
        if axis == 'y':
            target_y = self.curr_y + change
            target_x = self.curr_x
        elif axis == 'x':
            target_y = self.curr_y
            target_x = self.curr_x + change
        else:
            raise Exception("Unexpected direction: %s" % str(axis))
        if mode == _DRY_RUN:
            for boulder in univ.boulders:
                if boulder.curr_y == target_y and boulder.curr_x == target_x:
                    return boulder
            return univ.level_map[target_y][target_x]
        elif mode == _DO_MOVE:
            self.curr_y = target_y
            self.curr_x = target_x
            return univ.level_map[self.curr_y][self.curr_x]
        else:
            raise Exception("Unexpected move mode: %s" % str(mode))


class Boulder(_Movable):

    def move(self, move_dir, univ):
        mov = super(Boulder, self).move(move_dir, univ, _DRY_RUN)
        if mov in self.pushable:
            super(Boulder, self).move(move_dir, univ, _DO_MOVE)
            if mov == self.level_sym["Pit"]:
                univ.level_map[self.curr_y][self.curr_x] = \
                    self.level_sym["Floor"]
                univ.pits_remaining -= 1
            return mov


class Player(_Movable):

    def move(self, move_dir, univ):
        player_move_result = super(Player, self).move(
            move_dir,
            univ,
            _DRY_RUN,
        )
        if player_move_result in self.walkable:
            super(Player, self).move(move_dir, univ, _DO_MOVE)
            univ.moves_taken += 1
        if isinstance(player_move_result, Boulder):
            boulder_move_sq = player_move_result.move(move_dir, univ)
            if boulder_move_sq in self.pushable:
                super(Player, self).move(move_dir, univ, _DO_MOVE)
                univ.moves_taken += 1
                if boulder_move_sq == self.level_sym['Pit']:
                    univ.delete_boulder(player_move_result)
