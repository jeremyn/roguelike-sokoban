# Copyright 2020, Jeremy Nation <jeremy@jeremynation.me>
# Released under the GPLv3. See included LICENSE file.
import sqlite3
import unittest

from src import main
from src.score_tracking import ScoreTracker


class TestScoreTracker(unittest.TestCase):

    def test_get_best_score_none(self):
        score_tracker = ScoreTracker(':memory:', 'my_file', 'my_level')
        self.assertEquals(score_tracker.get_best_score(), None)

    def test_update_best_score(self):
        score_tracker = ScoreTracker(':memory:', 'my_file', 'my_level')
        score_tracker.update_best_score(10)
        self.assertEquals(score_tracker.get_best_score(), 10)

    def test_update_best_score_with_better_score(self):
        score_tracker = ScoreTracker(':memory:', 'my_file', 'my_level')
        score_tracker.update_best_score(10)
        score_tracker.update_best_score(5)
        self.assertEqual(score_tracker.get_best_score(), 5)

    def test_update_best_score_with_worse_score(self):
        score_tracker = ScoreTracker(':memory:', 'my_file', 'my_level')
        score_tracker.update_best_score(10)
        score_tracker.update_best_score(15)
        self.assertEqual(score_tracker.get_best_score(), 10)

    def test_close(self):
        score_tracker = ScoreTracker(':memory:', 'my_file', 'my_level')
        score_tracker.close()
        with self.assertRaises(sqlite3.ProgrammingError):
            score_tracker.get_best_score()

if __name__ == '__main__':
    unittest.main()
