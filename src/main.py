"""
Copyright 2021, Jeremy Nation <jeremy@jeremynation.me>
Released under the GPLv3. See included LICENSE file.

"""
import curses
from pathlib import Path

from src.display import Display
from src.levelloader import LevelLoader
from src.score_tracking import Scores
from src.universe import Universe
from src.util import SCORES_FILENAME, Action


def main(
    scrn: curses.window,
    level_filename: Path,
    update_scores: bool = True,
) -> None:
    if curses.has_colors():
        curses.use_default_colors()

    if update_scores:
        scores = Scores(SCORES_FILENAME)
    else:
        scores = Scores()

    loader = LevelLoader(level_filename)
    level_name = None
    keep_playing = True
    while keep_playing:
        if level_name is None:
            level_name = loader.level_prompt(scrn)
        univ = Universe(level_name, loader.levels[level_name], loader.symbols)
        best_score = scores.get_score(level_filename, univ.level_name)
        disp = Display(scrn, univ, best_score)
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
                            level_filename, univ.level_name, univ.moves_taken
                        )
