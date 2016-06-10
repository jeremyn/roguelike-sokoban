#!/usr/bin/env python
#
# Copyright 2016, Jeremy Nation <jeremy@jeremynation.me>
# Released under the GPLv3. See included LICENSE file.
import argparse

import textwrap
import curses
import src
import src.constants as const


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-L',
        '--level-file',
        nargs='?',
        default=const.DEFAULT_LEVEL_FILE_NAME_FULL,
        dest='level_filename',
        help="load specified level file (default: %(default)s)",
        metavar='FILE',
    )
    args = parser.parse_args()

    try:
        curses.wrapper(src.main, args.level_filename)
    except KeyboardInterrupt:
        final_msg = 'Exiting at user request. Thanks for playing!'
    except src.display.WindowTooSmallError:
        final_msg = """
            Error: window too small. Please increase your terminal size to at
            least 80x24 and try again.
        """
    except src.levelloader.MalformedLevelFileError as e:
        final_msg = """
            Problem with contents of level file: %(error_msg)s

            This error means there is something wrong with a custom level file
            you are trying to use. Please correct that file as needed using
            the hints in the included level file '%(level_filename)s' and try
            again.
        """ % {
            'error_msg': str(e),
            'level_filename': const.DEFAULT_LEVEL_FILE_NAME,
        }
    except src.levelloader.LevelFileHandlingError as e:
        final_msg = """
            Level file error: %(error_msg)s

            Check file permissions and other possible file-related issues and
            try again.
        """ % {
            'error_msg': str(e),
        }

    lines = str.splitlines(final_msg)
    for line in lines:
        print(textwrap.fill(line.strip()))
