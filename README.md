# Roguelike Sokoban

By: [Jeremy Nation](mailto:jeremy@jeremynation.me).

## Description

Roguelike Sokoban is an ASCII-based Sokoban game that has a look and feel inspired by the roguelike genre, particularly the Sokoban levels in the excellent game [NetHack](https://www.nethack.org/). You can create new maps using a regular text editor.

## Python version

Python 3.9. No external dependencies are needed, but the game requires the `curses` library which is not included with Python for Windows, though you can use [WSL](https://docs.microsoft.com/en-us/windows/wsl/).

## Running Roguelike Sokoban

Run

    python3.9 rlsokoban.py

from the root repository directory to play the default levels. To specify a level file, use the `-L` option followed by the path to the level file.

## Included levels

By default, the game will use the level file `levels/default-levels.txt`. Also included are many levels that have been adapted from the game [XSokoban](http://www.cs.cornell.edu/andru/xsokoban.html), which has been released into the public domain. These levels are included as `levels/xsokoban$X-$Y.txt` and can be loaded with the `-L` option.

*Note*: the XSokoban levels were converted using the included `convert_xsokoban.py` script and have not all been playtested. They were originally written to use a different set of Sokoban rules than Roguelike Sokoban uses. It is possible some of them are unwinnable from the start. Please let me know if one of the included levels is unwinnable.

## Development/Testing

`requirements-dev.txt` has various formatting/linting packages you can install with pip.

You can run the included tests with

    python3.9 run_tests.py

By default, this will just run unit tests, but you can also play test levels by using the `--include-manual-tests` option.

## License

Copyright [Jeremy Nation](mailto:jeremy@jeremynation.me).

Licensed under the GNU General Public License (GPL) v3. See the included [`LICENSE`](LICENSE) file for the full license text.
