"""
Copyright 2021, Jeremy Nation <jeremy@jeremynation.me>
Released under the GPLv3. See included LICENSE file.

"""
import json
from typing import Optional


class Scores(object):
    def __init__(self, db_file_name: Optional[str] = None):
        self._db_file_name = db_file_name
        self._scores: dict[str, dict[str, int]]
        if self._db_file_name is None:
            self._scores = {}
        else:
            try:
                with open(self._db_file_name) as score_file:
                    self._scores = json.load(score_file)
            except FileNotFoundError:
                self._scores = {}

    def get_best_score(self, level_file_name: str, level_name: str) -> Optional[int]:
        try:
            best_score: Optional[int] = self._scores[level_file_name][level_name]
        except KeyError:
            best_score = None
        return best_score

    def update_best_score(
        self, level_file_name: str, level_name: str, score: int
    ) -> None:
        current_best_score = self.get_best_score(level_file_name, level_name)
        updated = True
        if current_best_score is None:
            if level_file_name in self._scores:
                self._scores[level_file_name][level_name] = score
            else:
                self._scores[level_file_name] = {level_name: score}
        else:
            if score < current_best_score:
                self._scores[level_file_name][level_name] = score
            else:
                updated = False

        if updated and self._db_file_name is not None:
            with open(self._db_file_name, mode="w") as score_file:
                json.dump(self._scores, score_file, sort_keys=True, indent=2)
                score_file.write("\n")
