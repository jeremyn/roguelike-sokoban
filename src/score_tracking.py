"""
Copyright 2021, Jeremy Nation <jeremy@jeremynation.me>
Released under the GPLv3. See included LICENSE file.

"""
import filecmp
import json
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Optional

from src.util import UTF_8


class Scores(object):
    def __init__(self, scores_filename: Optional[Path] = None):
        self._scores_filename = scores_filename
        self._scores: dict[Path, dict[str, int]]
        if self._scores_filename is None:
            self._scores = {}
        else:
            try:
                self._scores = {
                    Path(k): v
                    for k, v in json.loads(
                        self._scores_filename.read_text(encoding=UTF_8)
                    ).items()
                }
            except FileNotFoundError:
                self._scores = {}

    def get_score(self, level_filename: Path, level_name: str) -> Optional[int]:
        level_filename = level_filename.resolve()
        try:
            best_score: Optional[int] = self._scores[level_filename][level_name]
        except KeyError:
            best_score = None
        return best_score

    def set_score(self, level_filename: Path, level_name: str, score: int) -> None:
        level_filename = level_filename.resolve()
        if level_filename in self._scores:
            self._scores[level_filename][level_name] = score
        else:
            self._scores[level_filename] = {level_name: score}

    def update_best_score(
        self, level_filename: Path, level_name: str, score: int
    ) -> None:
        current_best_score = self.get_score(level_filename, level_name)
        if (current_best_score is None) or (score < current_best_score):
            self.set_score(level_filename, level_name, score)
            if self._scores_filename is not None:
                # write first to a temp file so if the program crashes, we don't destroy
                # the existing score file
                with TemporaryDirectory() as temp_dir_str:
                    temp_filename = Path(temp_dir_str) / "new_scores.json"
                    with temp_filename.open(mode="w", encoding=UTF_8) as file:
                        json.dump(
                            {str(k): v for k, v in self._scores.items()},
                            file,
                            sort_keys=True,
                            indent=2,
                        )
                        file.write("\n")

                    files_match = False
                    try:
                        files_match = filecmp.cmp(temp_filename, self._scores_filename)
                    except FileNotFoundError:
                        pass
                    if not files_match:
                        temp_filename.rename(self._scores_filename)
