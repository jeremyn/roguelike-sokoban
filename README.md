# Roguelike Sokoban

By: [Jeremy Nation](mailto:jeremy@jeremynation.me)

## Description

Roguelike Sokoban is an ASCII-based Sokoban game that has a look and feel
inspired by the roguelike genre, particularly the Sokoban levels in the
excellent game [Nethack](http://www.nethack.org/). You can create new maps
using a regular text editor.

## Running Roguelike Sokoban

Roguelike Sokoban is written in Python and uses the
[curses](https://docs.python.org/2/library/curses.html) library for its
display. Install the pip packages in `requirements.txt`, or
`requirements-dev.txt` to include development-only packages, and then execute

    python rlsokoban.py

from the root repository directory to play the default levels. To specify a
level file, use the `-L` option followed by the path to the level file.

On Windows, you will need to install Python and then figure out how to make
curses available.

## Included levels

By default, the game will use the level file `levels/default-levels.yml`. Also
included are many levels that have been adapted from the game
[XSokoban](http://www.cs.cornell.edu/andru/xsokoban.html), which has been
released into the public domain. These levels are included as
`levels/xsokoban$X-$Y.yml` and can be loaded with the `-L` option.

*Note*: the XSokoban levels were converted using the included
`util/convert_xsokoban.py` script and have not all been playtested. They were
originally written to use a different set of Sokoban rules than Roguelike
Sokoban uses. It is possible some of them are unwinnable from the start. Please
let me know if one of the included levels is unwinnable.

## Testing

You can run the included tests with

    python run_tests.py

By default, this will just run unit tests, but you can run manual test levels by
adding the "--include-manual-tests" option.

## License

GPLv3 or later (see included `LICENSE` file).
