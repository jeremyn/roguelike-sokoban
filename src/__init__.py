# Copyright 2020, Jeremy Nation <jeremy@jeremynation.me>
# Released under the GPLv3. See included LICENSE file.

import curses

import action
import constants as const
import display
import gameobjects
import score_tracking
import levelloader


def main(scrn, level_file_name=const.DEFAULT_LEVEL_FILE_NAME_FULL):
    if curses.has_colors():
        curses.use_default_colors()
    disp = display.Display(scrn)
    loader = levelloader.LevelLoader(level_file_name)
    keep_playing = True
    name = None
    while keep_playing:
        univ = gameobjects.universe.Universe(loader.get_level(disp, name))
        score_tracker = score_tracking.ScoreTracker(
            const.SCORES_FILE_NAME,
            level_file_name,
            univ.level_name,
        )
        try:
            best_score = score_tracker.get_best_score()
            disp.level_init(univ, best_score)
            while True:
                disp.draw(univ)
                act = disp.get_action()
                if act == action.QUIT:
                    raise KeyboardInterrupt
                elif univ.game_won:
                    if act == action.PLAY_AGAIN:
                        name = None
                        break
                    else:
                        pass
                else:
                    if act == action.PLAY_AGAIN:
                        name = univ.level_name
                        break
                    elif act == action.OTHER:
                        pass
                    else:
                        univ.eval_action(act)
                        if univ.game_won:
                            score_tracker.update_best_score(univ.moves_taken)
        finally:
            score_tracker.close()
