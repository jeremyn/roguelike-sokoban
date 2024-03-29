"""
Copyright Jeremy Nation <jeremy@jeremynation.me>.
Licensed under the GNU General Public License (GPL) v3.

"""
import argparse
import curses
import unittest

from src.main import main
from src.util import QUIT, TEST_DIR, TEST_LEVELS_DIR

TEST_LEVELS = (
    TEST_LEVELS_DIR / "simple_level.txt",
    TEST_LEVELS_DIR / "different_symbols.txt",
    TEST_LEVELS_DIR / "huge_level.txt",
)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--include-manual-tests", action="store_true")
    args = parser.parse_args()

    test_loader = unittest.TestLoader().discover(str(TEST_DIR))
    unittest.TextTestRunner().run(test_loader)

    print()
    if args.include_manual_tests:
        input(
            f"Unit tests complete, press <ENTER> to run manual tests. (Pressing '{QUIT}' will move "
            "you to the next test level.) "
        )
        for test_level in TEST_LEVELS:
            try:
                curses.wrapper(main, level_filename=test_level, update_scores=False)
            except KeyboardInterrupt:
                pass
    else:
        print(
            "Unit tests complete, skipping manual tests. (Rerun with "
            "'--include-manual-tests' to include them.)"
        )

    print("All tests complete.")
