# Copyright 2020, Jeremy Nation <jeremy@jeremynation.me>
# Released under the GPLv3. See included LICENSE file.
import argparse
import curses

import src
from src.main import main


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-L',
        '--level-file',
        nargs='?',
        default=src.constants.DEFAULT_LEVEL_FILE_NAME_FULL,
        dest='level_filename',
        help="load specified level file (default: %(default)s)",
        metavar='FILE',
    )
    args = parser.parse_args()

    try:
        curses.wrapper(main, args.level_filename)
    except KeyboardInterrupt:
        print('Exiting at user request. Thanks for playing!')
