# Copyright 2021, Jeremy Nation <jeremy@jeremynation.me>
# Released under the GPLv3. See included LICENSE file.
import os
from collections import namedtuple
from enum import Enum

GAME_NAME = "Roguelike Sokoban"

DEFAULT_LEVEL_DIR = os.path.join(os.getcwd(), "levels")
DEFAULT_LEVEL_FILE_NAME = "default_levels.txt"
DEFAULT_LEVEL_FILE_NAME_FULL = os.path.join(
    DEFAULT_LEVEL_DIR,
    DEFAULT_LEVEL_FILE_NAME,
)

SCORES_FILE_NAME = "scores.json"

QUIT = "q"
PLAY_AGAIN = "r"


class Action(Enum):
    UP = "up"
    DOWN = "down"
    LEFT = "left"
    RIGHT = "right"
    QUIT = "quit"
    PLAY_AGAIN = "play again"
    OTHER = "other"


_LevelFileConsts = namedtuple(
    "LevelFileConsts",
    [
        "COMMENT_MARKER",
        "DELIMITER",
        "MAPS_START",
        "NAME_PREFIX",
    ],
)
LevelFileConsts = _LevelFileConsts(
    COMMENT_MARKER="#",
    DELIMITER=": ",
    MAPS_START="-> maps",
    NAME_PREFIX="name",
)
