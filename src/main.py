# Copyright 2021, Jeremy Nation <jeremy@jeremynation.me>
# Released under the GPLv3. See included LICENSE file.

import curses
import os

from src import constants as const
from src import display, levelloader, score_tracking, universe

Action = const.Action


def main(scrn, level_file_name=const.DEFAULT_LEVEL_FILE_NAME_FULL, update_scores=True):
    if curses.has_colors():
        curses.use_default_colors()
    disp = display.Display(scrn)
    loader = levelloader.LevelLoader(level_file_name)
    keep_playing = True
    base_level_filename = os.path.basename(level_file_name)
    level_name = None

    if update_scores:
        scores = score_tracking.Scores(const.SCORES_FILE_NAME)
    else:
        scores = score_tracking.Scores()

    while keep_playing:
        univ = universe.Universe(loader.get_level(disp, level_name))
        best_score = scores.get_best_score(base_level_filename, univ.level_name)
        disp.level_init(univ, best_score)
        while True:
            disp.draw(univ)
            act = disp.get_action()
            if act == Action.QUIT:
                raise KeyboardInterrupt
            elif univ.game_won:
                if act == Action.PLAY_AGAIN:
                    level_name = None
                    break
                else:
                    pass
            else:
                if act == Action.PLAY_AGAIN:
                    level_name = univ.level_name
                    break
                elif act == Action.OTHER:
                    pass
                else:
                    univ.eval_action(act)
                    if univ.game_won:
                        scores.update_best_score(
                            base_level_filename,
                            univ.level_name,
                            univ.moves_taken,
                        )
