# Copyright 2016, Jeremy Nation <jeremy@jeremynation.me>
# Released under the GPLv3. See included LICENSE file.
"""
Module with constants representing actions.

This module, like module constants, holds various constants used by Roguelike
Sokoban. However, these constants are specifically intended to abstract player
actions, so they've been put in their own module.

These values should not be modified by the casual user. 

"""

RESIZE = "resize"
UP = "up"
DOWN = "down"
LEFT = "left"
RIGHT = "right"
QUIT = "quit"
PLAY_AGAIN = "play again"
OTHER = "other"
