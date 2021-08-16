# Copyright 2021, Jeremy Nation <jeremy@jeremynation.me>
# Released under the GPLv3. See included LICENSE file.
import unittest

from src.score_tracking import Scores


class TestScoreTracker(unittest.TestCase):
    _filename: str
    _level_name: str

    @classmethod
    def setUpClass(cls) -> None:
        cls._filename = "my_file"
        cls._level_name = "my_level"
        return super().setUpClass()

    def test_get_best_score_none(self) -> None:
        scores = Scores()
        self.assertEquals(scores.get_best_score(self._filename, self._level_name), None)

    def test_update_best_score(self) -> None:
        scores = Scores()
        scores.update_best_score(self._filename, self._level_name, 10)
        self.assertEquals(scores.get_best_score(self._filename, self._level_name), 10)

    def test_update_best_score_with_better_score(self) -> None:
        scores = Scores()
        scores.update_best_score(self._filename, self._level_name, 10)
        scores.update_best_score(self._filename, self._level_name, 5)
        self.assertEqual(scores.get_best_score(self._filename, self._level_name), 5)

    def test_update_best_score_with_worse_score(self) -> None:
        scores = Scores()
        scores.update_best_score(self._filename, self._level_name, 10)
        scores.update_best_score(self._filename, self._level_name, 15)
        self.assertEqual(scores.get_best_score(self._filename, self._level_name), 10)


if __name__ == "__main__":
    unittest.main()
