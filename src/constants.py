# Copyright 2020, Jeremy Nation <jeremy@jeremynation.me>
# Released under the GPLv3. See included LICENSE file.
from enum import Enum
import os

GAME_NAME = 'Roguelike Sokoban'

DEFAULT_LEVEL_FILE_NAME = 'default_levels.yml'
DEFAULT_LEVEL_FILE_NAME_FULL = os.path.join(
    os.getcwd(),
    'levels',
    DEFAULT_LEVEL_FILE_NAME,
)

SCORES_FILE_NAME = os.path.join(
    os.getcwd(),
    'scores.sqlite3',
)

QUIT = 'q'
PLAY_AGAIN = 'r'

class Action(Enum):
    UP = "up"
    DOWN = "down"
    LEFT = "left"
    RIGHT = "right"
    QUIT = "quit"
    PLAY_AGAIN = "play again"
    OTHER = "other"
