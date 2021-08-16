# Copyright 2021, Jeremy Nation <jeremy@jeremynation.me>
# Released under the GPLv3. See included LICENSE file.
from src.constants import Action

_MOVE_TEST = {
    Action.UP: {"axis": "y", "change": -1},
    Action.DOWN: {"axis": "y", "change": 1},
    Action.LEFT: {"axis": "x", "change": -1},
    Action.RIGHT: {"axis": "x", "change": 1},
}
_DRY_RUN = "dry run"
_DO_MOVE = "do move"


class _Movable(object):
    def __init__(self, start_y, start_x, level_sym):
        self.curr_y = start_y
        self.curr_x = start_x
        self.level_sym = level_sym
        self.walkable = [self.level_sym["floor"]]
        self.pushable = self.walkable[:]
        self.pushable.append(self.level_sym["pit"])
        try:
            self.symbol = self.level_sym[self._SYMBOL_LOOKUP]
        except KeyError:
            raise Exception(
                "Unexpected _Movable derived class: %s" % self.__class__.__name__
            )

    def move(self, move_dir, univ, mode=None):
        axis = _MOVE_TEST[move_dir]["axis"]
        change = _MOVE_TEST[move_dir]["change"]
        if axis == "y":
            target_y = self.curr_y + change
            target_x = self.curr_x
        elif axis == "x":
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


class _Boulder(_Movable):

    _SYMBOL_LOOKUP = "boulder"

    def move(self, move_dir, univ):
        mov = super(_Boulder, self).move(move_dir, univ, _DRY_RUN)
        if mov in self.pushable:
            super(_Boulder, self).move(move_dir, univ, _DO_MOVE)
            if mov == self.level_sym["pit"]:
                univ.level_map[self.curr_y][self.curr_x] = self.level_sym["floor"]
                univ.pits_remaining -= 1
            return mov


class _Player(_Movable):

    _SYMBOL_LOOKUP = "player"

    def move(self, move_dir, univ):
        player_move_result = super(_Player, self).move(
            move_dir,
            univ,
            _DRY_RUN,
        )
        if player_move_result in self.walkable:
            super(_Player, self).move(move_dir, univ, _DO_MOVE)
            univ.moves_taken += 1
        if isinstance(player_move_result, _Boulder):
            boulder_move_sq = player_move_result.move(move_dir, univ)
            if boulder_move_sq in self.pushable:
                super(_Player, self).move(move_dir, univ, _DO_MOVE)
                univ.moves_taken += 1
                if boulder_move_sq == self.level_sym["pit"]:
                    univ.delete_boulder(player_move_result)


class Universe(object):
    def __init__(self, level_info):
        level_name, level_map, level_sym = level_info
        self.level_map = [list(line) for line in level_map]
        self.level_name = level_name
        self.level_sym = level_sym
        self.boulders = []
        self.pits_remaining = 0
        self.moves_taken = 0
        for row_index, row in enumerate(self.level_map):
            for col_index, square in enumerate(row):
                if square == self.level_sym["player"]:
                    self.player = _Player(
                        row_index,
                        col_index,
                        self.level_sym,
                    )
                    self.level_map[row_index][col_index] = self.level_sym["floor"]
                if square == self.level_sym["boulder"]:
                    self.boulders.append(
                        _Boulder(row_index, col_index, self.level_sym),
                    )
                    self.level_map[row_index][col_index] = self.level_sym["floor"]
                if square == self.level_sym["pit"]:
                    self.pits_remaining += 1
        self.__set_win_status()

    def eval_action(self, act):
        move_dir = act
        self.player.move(move_dir, self)
        self.__set_win_status()

    def delete_boulder(self, boulder):
        self.boulders.remove(boulder)

    def __set_win_status(self):
        self.game_won = self.pits_remaining == 0
