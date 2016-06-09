#!/usr/bin/env python
#
# Copyright 2016, Jeremy Nation <jeremy@jeremynation.me>
# Released under the GPLv3. See included LICENSE file.
"""
Script that converts XSokoban levels into Roguelike Sokoban-style level files.

The XSokoban levels seem to use standard Sokoban level formatting as described
here:

http://www.sokobano.de/wiki/index.php?title=Level_format

An example conversion is

    #####
    #   #
    #$  #
  ###  $##
  #  $ $ #
### # ## #   ######
#   # ## #####  ..#
# $  $          ..#
##### ### #@##  ..#
    #     #########
    #######

to

XSokoban level 1
    -----          
    |...|          
    |0..|          
  ---..0--         
  |..0.0.|         
---.|.--.|   ------
|...|.--.-----..^^|
|.0..0..........^^|
-----.---.|@--..^^|
    |.....---------
    -------        

However, Roguelike Sokoban gameplay is a variant on normal Sokoban gameplay
that is not always compatible with normal Sokoban. Specifically, normal
Sokoban allows you to move the player or boulders on and off pits, and boulders
do not fill in pits to make floor. So in normal Sokoban, it is valid to have a
player or a boulder starting on a pit, indicated in the standard format with +
or * respectively.

This script will not create a Roguelike Sokoban level if the XSokoban level
starts in an impossible condition for the Roguelike Sokoban type of play. The
script does this by making sure that the symbols in the converted map are all
"normal": wall, player, boulder, pit, floor, or blank.

Another problem with the typical Sokoban layout as far as Roguelike Sokoban is
concerned is that that it describes walls that the player cannot cross, while
Roguelike Sokoban describes the floor on which the player can move. This script
will draw the floor after inspecting the walls.

The levels created by this script have not all been playtested. It's possible
some of them are unwinnable.

The original (?) XSokoban has been released into the public domain. Its
homepage is

http://www.cs.cornell.edu/andru/xsokoban.html

The levels that this script produces came from XSokoban version 3.3c. The
output level files from this script are included in the levels directory as
xsokoban<x>-<y>dat.

This script can be used as a model to write your own script to convert
other Sokoban files to Roguelike Sokoban-style files.

"""
import copy
from functools import reduce
import os

# Standard format

S_WALL = "#"
S_PLAYER = "@"
S_PLAYER_ON_GOAL = "+"
S_BOX = "$"
S_BOX_ON_GOAL = "*"
S_GOAL = "."
S_FLOOR = " "

# Roguelike Sokoban format

RL_HORIZ_WALL = "-"
RL_VERT_WALL = "|"
RL_PLAYER = "@"
RL_BOULDER = "0"
RL_PIT = "^"
RL_FLOOR = "."

# Temp

TEMP_FLOOR = "F"


def rewrite_floor(level):
    """Do first pass for floors.

    Go through level and figure out which blanks are floor and which are
    just blanks. Change the floor-blanks to TEMP_FLOOR for later processing.
    Leave non-floor-blanks as they are.

    """
    objects = [S_WALL, S_PLAYER, S_BOX, S_GOAL]
    orig_level = copy.deepcopy(level)
    for row_num, row in enumerate(orig_level):
        for col_num, square in enumerate(row):
            if square == ' ':
                object_in_each_dir = True

                object_found = False
                for i in range(row_num, -1, -1):
                    if orig_level[i][col_num] in objects:
                        object_found = True
                        break
                object_in_each_dir = object_in_each_dir and object_found

                object_found = False
                for i in range(row_num, len(level)):
                    if orig_level[i][col_num] in objects:
                        object_found = True
                        break
                object_in_each_dir = object_in_each_dir and object_found

                object_found = False
                for j in range(col_num, -1, -1):
                    if orig_level[row_num][j] in objects:
                        object_found = True
                        break
                object_in_each_dir = object_in_each_dir and object_found

                object_found = False
                for j in range(col_num, len(row)):
                    if orig_level[row_num][j] in objects:
                        object_found = True
                        break
                object_in_each_dir = object_in_each_dir and object_found

                if object_in_each_dir:
                    level[row_num][col_num] = TEMP_FLOOR


def is_sideways_wall(level, i, j):
    """Return True if wall level[i][j] should be written with a "-", False
    otherwise.

    """
    # Set each value wall_x to 1 if there is a wall in x direction, 0 if not.
    if i > 0:
        wall_above = (level[i-1][j] == S_WALL) and 1 or 0
    else:
        wall_above = 0
    if i < len(level) - 1:
        wall_below = (level[i+1][j] == S_WALL) and 1 or 0
    else:
        wall_below = 0
    if j > 0:
        wall_left = (level[i][j-1] == S_WALL) and 1 or 0
    else:
        wall_left = 0
    if j < len(level[0]) - 1:
        wall_right = (level[i][j+1] == S_WALL) and 1 or 0
    else:
        wall_right = 0

    wall_status = [wall_above, wall_below, wall_left, wall_right]
    if sum(wall_status) == 1:
        if not (wall_above or wall_below):
            return True
    if sum(wall_status) == 2:
        if not (wall_above and wall_below):
            return True
    if sum(wall_status) == 3:
        return True
    return False


def rewrite_walls(level):
    """Rewrite walls.

    Go through level and rewrite each wall from "#" to either "-" or "|"
    depending on what other walls are around it. Uses is_sideways_wall(...).

    """
    orig_level = copy.deepcopy(level)
    for row_num, row in enumerate(orig_level):
        for col_num, square in enumerate(row):
            if square == S_WALL:
                if is_sideways_wall(orig_level, row_num, col_num):
                    level[row_num][col_num] = RL_HORIZ_WALL
                else:
                    level[row_num][col_num] = RL_VERT_WALL


def rewrite_final(level):
    """Finish rewriting.

    Go through level and finish rewriting, including rewriting TEMP_FLOOR to
    actual floor symbol RL_FLOOR.

    """
    orig_level = copy.deepcopy(level)
    for row_num, row in enumerate(orig_level):
        for col_num, square in enumerate(row):
            if square == S_PLAYER:
                level[row_num][col_num] = RL_PLAYER
            if square == S_BOX:
                level[row_num][col_num] = RL_BOULDER
            if square == S_GOAL:
                level[row_num][col_num] = RL_PIT
            if square == TEMP_FLOOR:
                level[row_num][col_num] = RL_FLOOR


def convert_one_level(filename):
    """Convert the XSokoban level in "filename" to Roguelike Sokoban-style.

    Convert the XSokoban level in "filename" to a list of strings that
    represents the level in Roguelike Sokoban-style. The first line in the
    list will be the level name "XSokoban level <number>".

    """
    try:
        level_file = open(filename)
    except NameError:
        raise NameError("could not open '%s'." % filename)
    level = level_file.readlines()
    level_file.close()
    max_line_length = reduce(max, [len(line)-1 for line in level])
    # Pad each line with spaces to the end of the longest line.
    orig_level = copy.deepcopy(level)
    for line_num, line in enumerate(orig_level):
        line = list(line)
        line.pop()  # Remove trailing '\n'
        while len(line) < max_line_length:
            line.append(' ')
        level[line_num] = line

    rewrite_floor(level)
    rewrite_walls(level)
    rewrite_final(level)

    level_name = "XSokoban level %s" % filename.split(".")[1]
    level.insert(0, level_name)

    return level


def is_good_level(level):
    """Return True if level has only valid RL characters, False otherwise."""
    valid_char = [
        RL_HORIZ_WALL,
        RL_VERT_WALL,
        RL_PLAYER,
        RL_BOULDER,
        RL_PIT,
        RL_FLOOR,
        ' ',
    ]
    # level[1:] to skip the name
    for line in level[1:]:
        for square in line:
            if square not in valid_char:
                return False
    return True

HEADER = "# The XSokoban website is:\n"\
         "# http://www.cs.cornell.edu/andru/xsokoban.html\n"\
         "#\n"\
         "# User-configurable symbols~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n"\
         "Floor = .\n"\
         "Pit = ^\n"\
         "Player = @\n"\
         "Boulder = 0\n"\
         "# Level maps below this line~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n"\

if __name__ == '__main__':
    os.chdir('../levels/screens')
    for i in range(1, 10):
        start = i*10-9
        end = i*10
        new_filename = "xsokoban%d-%d.dat" % (start, end)
        with open('../' + new_filename, 'w') as new_file:
            new_file.write(
                "# Levels based on XSokoban levels %d-%d.\n" % (start, end)
            )
            new_file.write('#\n')
            new_file.write(HEADER)
            for j in range(start, end+1):
                level = convert_one_level("screen.%d" % j)
                if is_good_level(level):
                    for line in level:
                        new_file.write(''.join(line) + '\n')
