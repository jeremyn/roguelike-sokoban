#!/usr/bin/env python
#
# Copyright 2016, Jeremy Nation <jeremy@jeremynation.me>
# Released under the GPLv3. See included LICENSE file.
import argparse

import sys
import traceback
import textwrap
import fcntl
import termios
import struct
import curses
import src
import src.constants as const


def print_wrap(text, length=None):
    if length is None:
        struct_in = struct.pack("HHHH", 0, 0, 0, 0)
        struct_out = fcntl.ioctl(sys.stdout, termios.TIOCGWINSZ, struct_in)
        term_dimensions = struct.unpack("HHHH", struct_out)
        length = term_dimensions[1] - 1
    length = min(length, 79)
    print(textwrap.fill(text, length))


def usage():
    print_wrap("")
    print_wrap("Options for %s:" % const.GAME_NAME)
    print_wrap("")
    print_wrap("no options   Play with defaults in %s" %
               const.DEFAULT_LEVEL_FILE_NAME_FULL)
    print_wrap("-h, --help   Display this usage information")
    print_wrap("-L <file>    Load specified level file rather than default")
    print_wrap("")

if __name__ == "__main__":
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
        print_wrap("Exiting at user request. Thanks for playing!")
    except src.display.WindowTooSmallError:
        print_wrap("Error: window too small. Please increase your terminal "
                   "size to at least 80x24 and try again.")
    except src.levelloader.MalformedLevelFileError as msg:
        print_wrap("Problem with contents of level file: %s" % str(msg))
        print_wrap("")
        print_wrap("This error means there is something wrong with a custom "
                   "level file you are trying to use. Please correct that "
                   "file as needed using the hints in the included level "
                   "file \'%s\' and try again." %
                   const.DEFAULT_LEVEL_FILE_NAME)
    except src.highscores.CorruptHighScoreFileError as msg:
        print_wrap("Problem with contents of high score file: %s" % str(msg))
        print_wrap("")
        print_wrap("This error means your high score file \'%s\' is "
                   "corrupt. Manually modifying the high score file can "
                   "leave it in a corrupt state. If there are any \'%s\' "
                   "files in the main game directory, you can try renaming "
                   "them to \'%s\' and restarting the game. This may load "
                   "good (older) data. Otherwise, you will need to remove "
                   "your existing \'%s\' file so the game can create a fresh "
                   "file. If you think this problem is the result of a "
                   "software bug, please report this on the %s issue tracker "
                   "at" % (const.DEFAULT_HIGH_SCORE_FILE_NAME_FULL,
                           const.HIGH_SCORE_EXTENSION,
                           const.DEFAULT_HIGH_SCORE_FILE_NAME,
                           const.DEFAULT_HIGH_SCORE_FILE_NAME,
                           const.GAME_NAME))
        print_wrap("")
        print_wrap(const.ISSUE_TRACKER)
        print_wrap("")
        print_wrap("and save the corrupt high score file for later debugging.")
    except src.highscores.HighScoreFileHandlingError as msg:
        print_wrap("High score file error: %s" % str(msg))
        print_wrap("")
        print_wrap("Check file permissions and other possible file-related "
                   "issues and try again.")
    except src.levelloader.LevelFileHandlingError as msg:
        print_wrap("Level file error: %s" % str(msg))
        print_wrap("")
        print_wrap("Check file permissions and other possible file-related "
                   "issues and try again.")
    except:
        traceback.print_exc()
        print_wrap("Unexpected error occurred! Please visit the %s issue "
                   "tracker at" % const.GAME_NAME)
        print_wrap("")
        print_wrap(const.ISSUE_TRACKER)
        print_wrap("")
        print_wrap("and report this as a new issue if it has not already "
                   "been reported. Please include all error information "
                   "along with a description of what was happening in the "
                   "game leading up to the crash. Your feedback is greatly "
                   "appreciated!")
