"""
Copyright 2021, Jeremy Nation <jeremy@jeremynation.me>
Released under the GPLv3. See included LICENSE file.

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

The 90 levels from XSokoban version 3.3c, processed by this script, are included as
levels/xsokoban<x>-<y>.txt. An original XSokoban file is also included for testing, see
the test code for more information.

"""
import argparse
import copy
from pathlib import Path

from src.levelloader import LevelsStr
from src.util import UTF_8, LevelFileConsts

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

_Level = list[list[str]]


def rewrite_floor(level: _Level) -> None:
    """Do first pass for floors.

    Go through level and figure out which blanks are floor and which are
    just blanks. Change the floor-blanks to TEMP_FLOOR for later processing.
    Leave non-floor-blanks as they are.

    """
    objects = [S_WALL, S_PLAYER, S_BOX, S_GOAL]
    orig_level = copy.deepcopy(level)
    for row_num, row in enumerate(orig_level):
        for col_num, square in enumerate(row):
            if square == " ":
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


def is_sideways_wall(level: _Level, i: int, j: int) -> bool:
    """Return True if wall level[i][j] should be written with a "-", False
    otherwise.

    """
    # Set each value wall_x to True if there is a wall in x direction, False if not.
    wall_above = (i > 0) and (level[i - 1][j] == S_WALL)
    wall_below = (i < len(level) - 1) and (level[i + 1][j] == S_WALL)
    wall_left = (j > 0) and (level[i][j - 1] == S_WALL)
    wall_right = (j < len(level[0]) - 1) and (level[i][j + 1] == S_WALL)

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


def rewrite_walls(level: _Level) -> None:
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


def rewrite_final(level: _Level) -> None:
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


def convert_one_level(filename: Path) -> tuple[str, _Level]:
    """Convert the XSokoban level in "filename" to Roguelike Sokoban-style.

    Convert the XSokoban level in "filename" to a list of strings that
    represents the level in Roguelike Sokoban-style. The first line in the
    list will be the level name "XSokoban level <number>".

    """
    with filename.open(encoding=UTF_8) as file:
        orig_level = file.readlines()
    max_line_length = max([len(line) - 1 for line in orig_level])
    # Pad each line with spaces to the end of the longest line.
    level: _Level = []
    for orig_line in orig_level:
        line = list(orig_line)
        line.pop()  # Remove trailing '\n'
        while len(line) < max_line_length:
            line.append(" ")
        level.append(line)

    rewrite_floor(level)
    rewrite_walls(level)
    rewrite_final(level)

    # [1:] skips the leading '.'
    level_name = f"XSokoban level {filename.suffix[1:]}"

    return level_name, level


def is_good_level(level: _Level) -> bool:
    """Return True if level has only valid RL characters, False otherwise."""
    valid_char = [
        RL_HORIZ_WALL,
        RL_VERT_WALL,
        RL_PLAYER,
        RL_BOULDER,
        RL_PIT,
        RL_FLOOR,
        " ",
    ]
    # level[1:] to skip the name
    for line in level[1:]:
        for square in line:
            if square not in valid_char:
                return False
    return True


def get_level_groups(max_level: int) -> list[tuple[int, int]]:
    """Get level groups.

    For example, if max_levels is 23, level groups will be [(1, 10), (11, 20), (21, 23)].

    """
    level_groups: list[tuple[int, int]] = []
    if max_level // 10:
        level_groups += [(i * 10 - 9, i * 10) for i in range(1, (max_level // 10) + 1)]

    if max_level % 10:
        level_groups += [(max_level + 1 - max_level % 10, max_level)]

    return level_groups


def main(args: argparse.Namespace) -> None:
    """Main function for script."""
    input_dir: Path = args.input_dir
    max_level: int = args.max_level
    output_dir: Path = args.output_dir if args.output_dir else input_dir
    delimiter = LevelFileConsts.DELIMITER + " "

    for start, end in get_level_groups(max_level):
        levels: LevelsStr = []
        for j in range(start, end + 1):
            level_name, level_lines = convert_one_level(input_dir / f"screen.{j}")
            if is_good_level(level_lines):
                levels.append(
                    {
                        "name": level_name.strip(),
                        "map": "\n".join(
                            ["".join(line).rstrip() for line in level_lines]
                        )
                        + "\n",
                    }
                )

        output_filename = output_dir / f"xsokoban{start}-{end}.txt"
        with output_filename.open(mode="w", encoding=UTF_8) as file:
            file.writelines(
                (
                    f"boulder{delimiter}{RL_BOULDER}\n",
                    f"floor{delimiter}{RL_FLOOR}\n",
                    f"pit{delimiter}{RL_PIT}\n",
                    f"player{delimiter}{RL_PLAYER}\n",
                    f"{LevelFileConsts.MAPS_START}\n",
                )
            )
            for level in levels:
                data = [
                    f"{LevelFileConsts.NAME_PREFIX}{delimiter}{level['name']}\n",
                    level["map"],
                ]
                file.writelines(data)


def get_parser() -> argparse.ArgumentParser:
    """Get the argparse parser."""
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "input_dir",
        help="input directory with XSokoban maps, containing files like 'screen.1'",
        metavar="input-dir",
        type=Path,
    )
    parser.add_argument("--max-level", default=90, help="max level", type=int)
    parser.add_argument(
        "--output-dir",
        help="output directory, defaults to input directory",
        type=Path,
    )
    return parser


if __name__ == "__main__":
    main(get_parser().parse_args())
