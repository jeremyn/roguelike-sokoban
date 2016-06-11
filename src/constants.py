# Copyright 2016, Jeremy Nation <jeremy@jeremynation.me>
# Released under the GPLv3. See included LICENSE file.
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
