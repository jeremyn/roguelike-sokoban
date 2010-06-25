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
AUTHOR = "Jeremy Nation <jeremy@jeremynation.me>"
AUTHOR_EMAIL = "jeremy@jeremynation.me"
COPYRIGHT = "Copyright 2010, Jeremy Nation"
LICENSE = "GPL"
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

# Metadata
__author__ = AUTHOR
__email__ = AUTHOR_EMAIL
__copyright__ = COPYRIGHT
__license__ = LICENSE
__version__ = VERSION
