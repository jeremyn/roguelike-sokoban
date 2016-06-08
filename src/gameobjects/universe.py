# Copyright 2016, Jeremy Nation <jeremy@jeremynation.me>
# Released under the GPLv3. See included LICENSE file.
import movable


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
                if square == self.level_sym["Player"]:
                    self.player = movable.Player(row_index, col_index,
                            self.level_sym)
                    self.level_map[row_index][col_index] = \
                            self.level_sym["Floor"]
                if square == self.level_sym["Boulder"]:
                    self.boulders.append(movable.Boulder(row_index, col_index,
                            self.level_sym))
                    self.level_map[row_index][col_index] = \
                            self.level_sym["Floor"]
                if square == self.level_sym["Pit"]:
                    self.pits_remaining += 1
        self.__set_win_status()

    def eval_action(self, act):
        move_dir = act
        self.player.move(move_dir, self)
        self.__set_win_status()

    def delete_boulder(self, boulder):
        self.boulders.remove(boulder)
        
    def __set_win_status(self):
        self.game_won = (self.pits_remaining == 0)
