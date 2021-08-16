"""
Copyright 2021, Jeremy Nation <jeremy@jeremynation.me>
Released under the GPLv3. See included LICENSE file.

"""
import json
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from src.score_tracking import Scores
from src.util import UTF_8


class TestScoreTracker(unittest.TestCase):
    _filename: Path
    _level_name: str

    @classmethod
    def setUpClass(cls) -> None:
        cls._filename = Path("my_file")
        cls._level_name = "my_level"
        return super().setUpClass()

    def test_set_get_score(self) -> None:
        scores = Scores()
        self.assertEqual(scores.get_score(self._filename, self._level_name), None)

        scores.set_score(self._filename, self._level_name, 1)
        self.assertEqual(scores.get_score(self._filename, self._level_name), 1)

        scores.set_score(self._filename, self._level_name, 2)
        self.assertEqual(scores.get_score(self._filename, self._level_name), 2)

    def test_update_best_score(self) -> None:
        scores = Scores()
        scores.update_best_score(self._filename, self._level_name, 10)
        self.assertEqual(scores.get_score(self._filename, self._level_name), 10)

    def test_update_best_score_with_better_score(self) -> None:
        scores = Scores()
        scores.update_best_score(self._filename, self._level_name, 10)
        scores.update_best_score(self._filename, self._level_name, 5)
        self.assertEqual(scores.get_score(self._filename, self._level_name), 5)

    def test_update_best_score_with_worse_score(self) -> None:
        scores = Scores()
        scores.update_best_score(self._filename, self._level_name, 10)
        scores.update_best_score(self._filename, self._level_name, 15)
        self.assertEqual(scores.get_score(self._filename, self._level_name), 10)

    def test_update_best_score_file(self) -> None:
        with TemporaryDirectory() as temp_dir_str:
            filename = Path(temp_dir_str) / "test_scores.json"
            scores = Scores(filename)

            scores.update_best_score(filename, self._level_name, 10)
            with filename.open(encoding=UTF_8) as file:
                scores_data = json.load(file)
            self.assertEqual({str(filename): {self._level_name: 10}}, scores_data)

            scores.update_best_score(filename, self._level_name, 5)
            with filename.open(encoding=UTF_8) as file:
                scores_data = json.load(file)
            self.assertEqual({str(filename): {self._level_name: 5}}, scores_data)

            second_level_name = self._level_name + "x"
            scores.update_best_score(filename, second_level_name, 15)
            with filename.open(encoding=UTF_8) as file:
                scores_data = json.load(file)
            self.assertEqual(
                {str(filename): {second_level_name: 15, self._level_name: 5}},
                scores_data,
            )


if __name__ == "__main__":
    unittest.main()
