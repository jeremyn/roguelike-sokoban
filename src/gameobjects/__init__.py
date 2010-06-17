"""Package 'gameobjects' containing modules relating to abstract game world
objects.

Contains:

movable : Module containing objects that represent movable things in Roguelike
    Sokoban.
    
universe : Module defining the Universe class for Roguelike Sokoban.

"""

import movable
import universe
from .. import constants as const

__author__ = const.AUTHOR
__email__ = const.AUTHOR_EMAIL
__copyright__ = const.COPYRIGHT
__license__ = const.LICENSE
__version__ = const.VERSION