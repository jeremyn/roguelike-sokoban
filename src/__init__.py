# Copyright 2016, Jeremy Nation <jeremy@jeremynation.me>
# Released under the GPLv3. See included LICENSE file.

import curses

import action
import constants as const
import display
import gameobjects
import highscores
import levelloader


def main(scrn, level_file_name=const.DEFAULT_LEVEL_FILE_NAME_FULL):
    if curses.has_colors():
        curses.use_default_colors()
    disp = display.Display(scrn)
    loader = levelloader.LevelLoader(level_file_name)
    hs = highscores.HighScores()
    keep_playing = True
    name = None
    while keep_playing:
        univ = gameobjects.universe.Universe(loader.get_level(disp, name))
        high_score = hs.get_high_score(level_file_name, univ.level_name)
        disp.level_init(univ, high_score)
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
                    if univ.game_won and (univ.moves_taken < high_score or
                                          high_score == const.NO_SCORE_SET):
                        hs.set_high_score(level_file_name, univ.level_name,
                                          univ.moves_taken)
                        hs.save_high_scores()
