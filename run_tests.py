# Copyright 2020, Jeremy Nation <jeremy@jeremynation.me>
# Released under the GPLv3. See included LICENSE file.
import argparse
import curses
import os
import unittest

import src
from test.test_levelloader import TestLevelLoader
from test.test_scoretracker import TestScoreTracker

TEST_DIR = 'test'
TEST_LEVELS_DIR = os.path.join(TEST_DIR, 'test_levels')
TEST_LEVELS = (
    os.path.join(TEST_LEVELS_DIR, 'simple_level.yml'),
    os.path.join(TEST_LEVELS_DIR, 'different_symbols.yml'),
    os.path.join(TEST_LEVELS_DIR, 'huge_level.yml'),
)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--include-manual-tests', action='store_true')
    args = parser.parse_args()

    test_loader = unittest.TestLoader().discover(TEST_DIR)
    unittest.TextTestRunner().run(test_loader)

    print()
    if args.include_manual_tests:
        input(
            "Unit tests complete, press <ENTER> to run manual tests. (Pressing "
            "'{const_quit}' will move you to the next test level.) ".format(
                const_quit=src.constants.QUIT,
            )
        )
        for test_level in TEST_LEVELS:
            try:
                curses.wrapper(src.main, test_level)
            except KeyboardInterrupt:
                pass
    else:
        print(
            "Unit tests complete, skipping manual tests. (Rerun with "
            "'--include-manual-tests' to include them.)"
        )

    print('All tests complete.')
