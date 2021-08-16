"""
Copyright 2021, Jeremy Nation <jeremy@jeremynation.me>
Released under the GPLv3. See included LICENSE file.

"""
import argparse
import curses
from pathlib import Path

from src.main import main
from src.util import DEFAULT_LEVEL_FILENAME

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-L",
        "--level-file",
        nargs="?",
        default=DEFAULT_LEVEL_FILENAME,
        dest="level_filename",
        help="load specified level file (default: %(default)s)",
        metavar="FILE",
        type=Path,
    )
    args = parser.parse_args()

    try:
        curses.wrapper(main, args.level_filename)
    except KeyboardInterrupt:
        print("Exiting at user request. Thanks for playing!")
