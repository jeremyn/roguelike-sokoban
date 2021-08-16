# Copyright 2021, Jeremy Nation <jeremy@jeremynation.me>
# Released under the GPLv3. See included LICENSE file.
import argparse
import curses
import os
import unittest

from src import constants as const
from src.main import main

TEST_DIR = "test"
TEST_LEVELS_DIR = os.path.join(TEST_DIR, "test_levels")
TEST_LEVELS = (
    os.path.join(TEST_LEVELS_DIR, "simple_level.txt"),
    os.path.join(TEST_LEVELS_DIR, "different_symbols.txt"),
    os.path.join(TEST_LEVELS_DIR, "huge_level.txt"),
)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--include-manual-tests", action="store_true")
    args = parser.parse_args()

    test_loader = unittest.TestLoader().discover(TEST_DIR)
    unittest.TextTestRunner().run(test_loader)

    print()
    if args.include_manual_tests:
        input(
            "Unit tests complete, press <ENTER> to run manual tests. (Pressing "
            "'{const_quit}' will move you to the next test level.) ".format(
                const_quit=const.QUIT,
            )
        )
        for test_level in TEST_LEVELS:
            try:
                curses.wrapper(main, level_file_name=test_level, update_scores=False)
            except KeyboardInterrupt:
                pass
    else:
        print(
            "Unit tests complete, skipping manual tests. (Rerun with "
            "'--include-manual-tests' to include them.)"
        )

    print("All tests complete.")
