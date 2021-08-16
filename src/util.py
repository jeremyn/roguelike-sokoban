"""
Copyright 2021, Jeremy Nation <jeremy@jeremynation.me>
Released under the GPLv3. See included LICENSE file.

"""
import os
from enum import Enum
from typing import NamedTuple

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

TERMINAL_TOO_SMALL_TEXT = (
    "Your terminal is too small. Please increase your terminal size to at "
    "least 80x24 and try again."
)


class Action(Enum):
    UP = "up"
    DOWN = "down"
    LEFT = "left"
    RIGHT = "right"
    QUIT = "quit"
    PLAY_AGAIN = "play again"
    OTHER = "other"


class _LevelFileConsts(NamedTuple):
    COMMENT_MARKER: str = "#"
    DELIMITER: str = ": "
    MAPS_START: str = "-> maps"
    NAME_PREFIX: str = "name"


LevelFileConsts = _LevelFileConsts()
