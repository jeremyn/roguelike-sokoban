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
Module with constants representing actions.

This module, like module constants, holds various constants used by Roguelike
Sokoban. However, these constants are specifically intended abstract player
actions, so they've been put in their own module.

These values should not be modified by the casual user. 

"""

import constants as const

__author__ = const.AUTHOR
__email__ = const.AUTHOR_EMAIL
__copyright__ = const.COPYRIGHT
__license__ = const.LICENSE
__version__ = const.VERSION
        
RESIZE = "resize"
UP = "up"
DOWN = "down"
LEFT = "left"
RIGHT = "right"
QUIT = "quit"
PLAY_AGAIN = "play again"
OTHER = "other"