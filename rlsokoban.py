"""
Copyright Jeremy Nation <jeremy@jeremynation.me>.
Licensed under the GNU General Public License (GPL) v3.

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
