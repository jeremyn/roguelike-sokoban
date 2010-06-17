#!/usr/bin/python -B
#
# Copyright 2010, Jeremy Nation <jeremy@jeremynation.me>
#
# This file is part of Roguelike Sokoban.
#
# Roguelike Sokoban is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Roguelike Sokoban is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Roguelike Sokoban.  If not, see <http://www.gnu.org/licenses/>.
"""
The main executable for Roguelike Sokoban.

Full documentation for Roguelike Sokoban can be found in README in the main 
directory.

Command-line options and usage for this executable can be found by running 

rlsokoban --help

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

__author__ = const.AUTHOR
__email__ = const.AUTHOR_EMAIL
__copyright__ = const.COPYRIGHT
__license__ = const.LICENSE
__version__ = const.VERSION

def print_wrap(text, length = None):
    """Print string with word wrapping.
    
    Input:
    
    text : string to print.
    
    length : word wrap length as integer. Defaults to None (the function will
        determine the length from the terminal width if a length is not
        specified).
    
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
    print textwrap.fill(text, length)

def usage():
    """Print usage information and exit."""
    print_wrap("")
    print_wrap("Options for " + const.GAME_NAME + ":")
    print_wrap("")
    print_wrap("no options   Play with defaults in " + \
        const.DEFAULT_LEVEL_FILE_NAME_FULL)
    print_wrap("-h, --help   Display this usage information")
    print_wrap("-L <file>    Load with specified level file rather than "\
               "default")
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
                print_wrap("Error: unknown option \"" + sys.argv[1] + "\".")
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
                print_wrap("Error: unknown option \"" + sys.argv[1] + "\".")
                usage()
        else: # len(sys.argv) == 1, use defaults
            curses.wrapper(src.main.main)
    except KeyboardInterrupt:
        print_wrap("Exiting at user request. Thanks for playing!")
    except src.display.WindowTooSmallError:
        print_wrap("Error: window too small. Please increase your terminal "
                   "size and try again.")
    except (src.levelloader.MalformedLevelFileError, IOError) as msg:
        print_wrap("Level file error: " + str(msg) + "")
        print_wrap("")
        print_wrap("This error probably means there is something wrong "\
                   "with a custom level file you are trying to use. Please "\
                   "correct that file as needed using the hints in the "\
                   "included level file \'" + const.DEFAULT_LEVEL_FILE_NAME + \
                   "\' and try again.")
    except:
        traceback.print_exc()
        print_wrap( "Unexpected error occurred! Please visit the " + \
              const.GAME_NAME + " issue tracker at\n\n" + \
              const.ISSUE_TRACKER + \
              "\n\nand report this error as a new issue. Please include all "\
              "error information along with a description of what was "\
              "happening in the game leading up to the crash.\n\nYour "\
              "feedback is greatly appreciated!")
