# Copyright 2016, Jeremy Nation <jeremy@jeremynation.me>
# Released under the GPLv3. See included LICENSE file.
"""
Module with non-user-modifiable constants for Roguelike Sokoban.

Module containing various constants for Roguelike Sokoban. These are not
intended to be modified by the casual user. User customization should be done
entirely through a custom level file (see the included levels.dat in the levels
directory for instructions). 

However, that said, the purpose of each of the constants in this module is
probably obvious, so feel free to tinker.

"""

import os

# Metadata constants
VERSION = "0.8.1"
GAME_NAME = "Roguelike Sokoban"
ISSUE_TRACKER = "http://github.com/jeremyn/Roguelike-Sokoban/issues"

# Level constants
MAX_LEVEL_NAME_LENGTH = 50
MAX_LEVELS_PER_FILE = 10
COMMENT = "#"
LEVEL_SYMBOL_TYPES = ("Floor", "Pit", "Player", "Boulder")
DEFAULT_LEVEL_FILE_NAME = "default_levels.dat"
DEFAULT_LEVEL_FILE_NAME_FULL = os.path.join(os.getcwd(), "levels", 
                                            DEFAULT_LEVEL_FILE_NAME)

# High score file

HIGH_SCORE_EXTENSION = ".sav"
DEFAULT_HIGH_SCORE_FILE_NAME = "high_scores" + HIGH_SCORE_EXTENSION
DEFAULT_HIGH_SCORE_FILE_NAME_FULL = os.path.join(os.getcwd(),
                                                 DEFAULT_HIGH_SCORE_FILE_NAME)
NO_SCORE_SET = 0

# Key options
QUIT = "q"
PLAY_AGAIN = "r"
