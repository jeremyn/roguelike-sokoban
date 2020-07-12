# Roguelike Sokoban

By: [Jeremy Nation](mailto:jeremy@jeremynation.me)

## Description

Roguelike Sokoban is an ASCII-based Sokoban game that has a look and feel
inspired by the roguelike genre, particularly the Sokoban levels in the
excellent game [NetHack](https://www.nethack.org/). You can create new maps
using a regular text editor.

## Python version

Please use a recent version of Python 3 when running anything in this
repository.

## Running Roguelike Sokoban

Run

    python rlsokoban.py

from the root repository directory to play the default levels. To specify a
level file, use the `-L` option followed by the path to the level file.

There is a `requirements-dev.txt` file you can install with `pip` if you want
packages only used for development.

Roguelike Sokoban uses the
[curses](https://docs.python.org/3/library/curses.html) module for its
display. `curses` isn't included in the Python distribution for Windows, so
on Windows you might want to use the
[Windows Subsystem for Linux](https://docs.microsoft.com/en-us/windows/wsl/) or
find some other option.

## Included levels

By default, the game will use the level file `levels/default-levels.txt`. Also
included are many levels that have been adapted from the game
[XSokoban](http://www.cs.cornell.edu/andru/xsokoban.html), which has been
released into the public domain. These levels are included as
`levels/xsokoban$X-$Y.txt` and can be loaded with the `-L` option.

*Note*: the XSokoban levels were converted using the included
`convert_xsokoban.py` script and have not all been playtested. They were
originally written to use a different set of Sokoban rules than Roguelike
Sokoban uses. It is possible some of them are unwinnable from the start.
Please let me know if one of the included levels is unwinnable.

## Testing

You can run the included tests with

    python run_tests.py

By default, this will just run unit tests, but you can run manual test levels by
adding the "--include-manual-tests" option.

## License

GPLv3 or later (see included `LICENSE` file).
