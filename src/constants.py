# Copyright 2016, Jeremy Nation <jeremy@jeremynation.me>
# Released under the GPLv3. See included LICENSE file.
import os

VERSION = '0.8.1'
GAME_NAME = 'Roguelike Sokoban'

MAX_LEVEL_NAME_LENGTH = 50
MAX_LEVELS_PER_FILE = 10
COMMENT = '#'
LEVEL_SYMBOL_TYPES = ('Floor', 'Pit', 'Player', 'Boulder')
DEFAULT_LEVEL_FILE_NAME = 'default_levels.dat'
DEFAULT_LEVEL_FILE_NAME_FULL = os.path.join(
    os.getcwd(),
    'levels',
    DEFAULT_LEVEL_FILE_NAME,
)

HIGH_SCORE_EXTENSION = '.sav'
DEFAULT_HIGH_SCORE_FILE_NAME = 'high_scores' + HIGH_SCORE_EXTENSION
DEFAULT_HIGH_SCORE_FILE_NAME_FULL = os.path.join(
    os.getcwd(),
    DEFAULT_HIGH_SCORE_FILE_NAME,
)
NO_SCORE_SET = 0

QUIT = 'q'
PLAY_AGAIN = 'r'
