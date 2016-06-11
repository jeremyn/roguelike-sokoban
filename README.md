# Roguelike Sokoban

By: Jeremy Nation <jeremy@jeremynation.me>

## Description

Roguelike Sokoban is an ASCII-based Sokoban game that has a look and feel
inspired by the roguelike genre. New maps with custom symbols can easily be
created using a regular text editor.

## Running Roguelike Sokoban

Roguelike Sokoban is written in Python and uses the curses library for its
display. Many popular Linux distributions come with Python by default, and
curses is included by default in the Python standard library for Linux. So if
you are using Linux and Python is already installed, just execute

    rlsokoban.py

from the main game directory to use the default maps. To use your own map file,
use the `-L` option followed by the name of your map file. Use either a
`--help` or `-h` option by itself to see command-line help.

Unfortunately, Python does not come with Windows by default, nor is curses
included in the Python standard library for Windows. So, if you are a Windows
user, you will need to work through a few things to get the game running. I am
even less certain about running this on a Mac. If anyone has any success with
running Roguelike Sokoban on either Windows or Mac, please let me know.

## Included levels

By default, the game will use the level file levels/default-levels.dat. Also
included however are 83 levels that have been adapted from the game
[XSokoban](http://www.cs.cornell.edu/andru/xsokoban.html), which has been
released into the public domain. These levels are included in the levels
directory as `xsokoban<x>-<y>.dat`. To play them, use the `-L` option. For
example,

    rlsokoban.py -L levels/xsokoban1-10.dat

will start the game with the ten levels in the level file xsokoban1-10.dat in
the levels directory.

*Note*: the XSokoban levels have not all been playtested. They were imported
into Roguelike Sokoban automatically using a script (see "Importing levels",
below).  They were originally written to use a slightly different set of
Sokoban rules than Roguelike Sokoban uses. It is possible some of them are
unwinnable from the start. Please see the documentation in the conversion
script mentioned in "Importing levels" for more information. If you find a
level that you think is unwinnable from the start, please visit the issue
tracker mentioned in "Known issues", below, and create a new issue for the
level (if an issue has not already been created for it).

## Writing your own levels

It is easy to create your own maps to use with Roguelike Sokoban using a
regular text editor. You simply type out the starting condition of the level,
and the game brings the level to life. The included levels.dat file in the
levels directory is heavily documented and provides examples. More examples,
including examples that will fail to load, can be found in the src/test
directory.

## Importing levels

There are many Sokoban levels available on the Internet. However, they are
typically not in a format that will work with Roguelike Sokoban. This release
includes a conversion script, `util/convert_xsokoban.py`, which was used to
convert XSokoban levels to Roguelike Sokoban levels. You can adapt this script
to import other levels. Please see the documentation at the top of that script
for more information.

## License

Roguelike Sokoban and all included files are copyright 2016, Jeremy Nation, and
licensed under the GNU General Public License v3, included in this release as
LICENSE.
