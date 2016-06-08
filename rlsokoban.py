#!/usr/bin/env python
#
# Copyright 2016, Jeremy Nation <jeremy@jeremynation.me>
# Released under the GPLv3. See included LICENSE file.
"""
The main executable for Roguelike Sokoban.

Full documentation for Roguelike Sokoban can be found in README in the main 
directory.

Command-line options and usage for this executable can be found by running 

rlsokoban.py --help

from the command line.

Functions :

print_wrap(text, length = None) : Print string with word wrapping.

usage() : Print usage information and exit.

"""

import sys
import traceback
import textwrap
import fcntl
import termios
import struct
import curses
import src
import src.constants as const


def print_wrap(text, length = None):
    """Print string with word wrapping.
    
    Input:
    
    text : string to print.
    
    length : word wrap length as integer. Defaults to None (the function will
        determine the length from the terminal width if a length is not
        specified). It will not wrap at any greater than 79 characters.
    
    """
    if length is None:
        # Pack a C struct with a format of four unsigned shorts.
        struct_in = struct.pack("HHHH", 0, 0, 0, 0)
        # Call fcntl.ioctl(...) and request terminal size with TIOCGWINSZ.
        struct_out = fcntl.ioctl(sys.stdout, termios.TIOCGWINSZ, struct_in)
        # Unpack struct_out to get terminal dimensions.
        term_dimensions = struct.unpack("HHHH", struct_out)
        # Terminal width is the second value in the 4-tuple.
        length = term_dimensions[1] - 1
    # Longer than 79 is too long to comfortably read on one line.
    length = min(length, 79)
    print textwrap.fill(text, length)

def usage():
    """Print usage information and exit."""
    print_wrap("")
    print_wrap("Options for %s:" % const.GAME_NAME)
    print_wrap("")
    print_wrap("no options   Play with defaults in %s" % 
               const.DEFAULT_LEVEL_FILE_NAME_FULL)
    print_wrap("-h, --help   Display this usage information")
    print_wrap("-L <file>    Load specified level file rather than default")
    print_wrap("")

if __name__ == "__main__":
    try:
        if len(sys.argv) > 3:
            print_wrap("")
            print_wrap("Error: wrong number of command line options.")
            usage()
        elif len(sys.argv) == 3:
            if sys.argv[1] != "-L":
                print_wrap("")
                print_wrap("Error: unknown option \'%s\'." % sys.argv[1])
                usage()
            else:
                curses.wrapper(src.main.main, sys.argv[2])
        elif len(sys.argv) == 2:
            if sys.argv[1] == "-h" or sys.argv[1] == "--help":
                usage()
            elif sys.argv[1] == "-L":
                print_wrap("")
                print_wrap("Error: option \"-L\" requires a file name.")
                usage()
            else:
                print_wrap("")
                print_wrap("Error: unknown option \'%s\'." % sys.argv[1])
                usage()
        else: # len(sys.argv) == 1, use defaults
            curses.wrapper(src.main.main)
    except KeyboardInterrupt:
        print_wrap("Exiting at user request. Thanks for playing!")
    except src.display.WindowTooSmallError:
        print_wrap("Error: window too small. Please increase your terminal "
                   "size to at least 80x24 and try again.")
    except src.levelloader.MalformedLevelFileError as msg:
        print_wrap("Problem with contents of level file: %s" % str(msg))
        print_wrap("")
        print_wrap("This error means there is something wrong with a custom "\
                   "level file you are trying to use. Please correct that "\
                   "file as needed using the hints in the included level "\
                   "file \'%s\' and try again." %
                   const.DEFAULT_LEVEL_FILE_NAME)
    except src.highscores.CorruptHighScoreFileError as msg:
        print_wrap("Problem with contents of high score file: %s" % str(msg))
        print_wrap("")
        print_wrap("This error means your high score file \'%s\' is "\
                   "corrupt. Manually modifying the high score file can "\
                   "leave it in a corrupt state. If there are any \'%s\' "\
                   "files in the main game directory, you can try renaming "\
                   "them to \'%s\' and restarting the game. This may load "\
                   "good (older) data. Otherwise, you will need to remove "\
                   "your existing \'%s\' file so the game can create a fresh "\
                   "file. If you think this problem is the result of a "\
                   "software bug, please report this on the %s issue tracker "\
                   "at" %(const.DEFAULT_HIGH_SCORE_FILE_NAME_FULL, 
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
        print_wrap("Check file permissions and other possible file-related "\
                   "issues and try again.")
    except src.levelloader.LevelFileHandlingError as msg:
        print_wrap("Level file error: %s" % str(msg))
        print_wrap("")
        print_wrap("Check file permissions and other possible file-related "\
                   "issues and try again.")
    except:
        traceback.print_exc()
        print_wrap("Unexpected error occurred! Please visit the %s issue "\
                   "tracker at" % const.GAME_NAME)
        print_wrap("")
        print_wrap(const.ISSUE_TRACKER)
        print_wrap("")
        print_wrap("and report this as a new issue if it has not already "\
                   "been reported. Please include all error information "\
                   "along with a description of what was happening in the "\
                   "game leading up to the crash. Your feedback is greatly "\
                   "appreciated!")
