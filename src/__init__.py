"""
Package 'src' containing most of the code for Roguelike Sokoban.

Packages:

gameobjects : Package containing modules relating to abstract game world
    objects.

Modules:

main : Module containing the main game loop for Roguelike Sokoban.

action : Module with constants representing actions.

constants : Module with non-user-modifiable constants for Roguelike Sokoban.

display : Display module for Roguelike Sokoban.

levelloader : Level loading module for Roguelike Sokoban.

highscores : Module that handles high scores.

"""

import main
import constants as const

__author__ = const.AUTHOR
__email__ = const.AUTHOR_EMAIL
__copyright__ = const.COPYRIGHT
__license__ = const.LICENSE
__version__ = const.VERSION