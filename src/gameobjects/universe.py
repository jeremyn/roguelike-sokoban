# Copyright 2010, Jeremy Nation <jeremy@jeremynation.me>
#
# This file is part of Roguelike Sokoban.
#
# Roguelike Sokoban is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Roguelike Sokoban is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Roguelike Sokoban.  If not, see <http://www.gnu.org/licenses/>.
"""
Module defining the Universe class for Roguelike Sokoban.

Classes:

Universe(object) : Class that holds the current state of the game world.

"""

import movable
from .. import constants as const

__author__ = const.AUTHOR
__email__ = const.AUTHOR_EMAIL
__copyright__ = const.COPYRIGHT
__license__ = const.LICENSE
__version__ = const.VERSION

class Universe(object):
    
    """Class that holds the current state of the game world.
    
    Methods:
    
    __init__(level_info) : Initialize game state with level_info.
    
    eval_action(act) : Updates the game status with the result of the user's
        action.
        
    delete_boulder(boulder) : Delete Boulder boulder from the Universe object.
    
    Data:
    
    level_name : name of the level as a string.
    
    level_map : list of lists of characters representing the static level map.
    
    level_sym : dictionary holding the symbol for each symbol type
    
    boulders : list containing all the current Boulder objects
    
    player : Player object
    
    pits_remaining : integer of how many pits still need to be filled
    
    moves_taken : integer of how many moves the player has taken
    
    game_won : boolean of whether the game is current in a won state

    """
    
    def __init__(self, level_info):
        """Initialize game state with level_info.
        
        Input:
        
        level_info : tuple of (level_name, level_map, level_sym) as returned
            by LevelLoader.get_level(...).
        
        """
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
        """Evaluate player action.
        
        This method evaluates the player's action and updates game_won. 
        
        Input:
        
        act : movement constant (UP, DOWN, LEFT, RIGHT) from module action.
        
        """
        move_dir = act
        self.player.move(move_dir, self)
        self.__set_win_status()

    def delete_boulder(self, boulder):
        """Delete Boulder boulder from the Universe object.
        
        Input:
        
        boulder : Boulder object to delete.
        
        """
        self.boulders.remove(boulder)
        
    def __set_win_status(self):
        """Update self.game_won.
        
        Sets self.game_win to True if game is in a won state, False otherwise.

        """
        self.game_won = (self.pits_remaining == 0)
