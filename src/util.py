"""
Copyright 2021, Jeremy Nation <jeremy@jeremynation.me>
Released under the GPLv3. See included LICENSE file.

"""
from enum import Enum
from pathlib import Path
from typing import NamedTuple

GAME_NAME = "Roguelike Sokoban"

DEFAULT_LEVEL_FILENAME = Path("levels") / "default_levels.txt"
SCORES_FILENAME = Path("scores.json")

QUIT = "q"
PLAY_AGAIN = "r"

TERMINAL_TOO_SMALL_TEXT = (
    "Your terminal is too small. Please increase your terminal size to at "
    "least 80x24 and try again."
)

TEST_DIR = Path("tests")
TEST_LEVELS_DIR = TEST_DIR / "test_levels"

UTF_8 = "utf-8"


class Action(Enum):
    """Represents actions the player can choose."""

    UP = "up"
    DOWN = "down"
    LEFT = "left"
    RIGHT = "right"
    QUIT = "quit"
    PLAY_AGAIN = "play again"
    OTHER = "other"


class _LevelFileConsts(NamedTuple):
    COMMENT_MARKER: str = "#"
    DELIMITER: str = ":"
    MAPS_START: str = "-> maps"
    NAME_PREFIX: str = "name"


LevelFileConsts = _LevelFileConsts()


class RoguelikeSokobanError(Exception):
    """Class for all game-specific errors."""
