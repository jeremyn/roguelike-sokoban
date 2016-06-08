# Copyright 2016, Jeremy Nation <jeremy@jeremynation.me>
# Released under the GPLv3. See included LICENSE file.
"""
Module containing objects that represent movable things in Roguelike Sokoban.

Classes:

Boulder(_Movable) : Class representing a boulder.

Player(_Movable) : Class representing the player.

"""

from .. import action


_MOVE_TEST = {
               action.UP: {"axis": "y", "change": -1},
               action.DOWN: {"axis": "y", "change": 1},
               action.LEFT: {"axis": "x", "change": -1},
               action.RIGHT: {"axis": "x", "change": 1},
               }
_DRY_RUN = "dry run"
_DO_MOVE = "do move"

class _Movable(object):
    
    """The base class from which movable objects in the world derive.
    
    Methods:
    
    __init__(start_y, start_x, level_sym) : Initialization method for 
        _Movable.
    
    move(move_dir, univ, mode): The basic move method that derived
        classes extend to move.
    
    """
    
    def __init__(self, start_y, start_x, level_sym):
        """Initialization method for _Movable.
        
        Input:
        
        start_y: the starting row of _Movable
        
        start_x: the starting column of _Movable
        
        level_sym: the dictionary of all symbols recognized by the game.
        
        The base _Movable class should never be instantiated, only its derived
        classes.
        
        """        
        self.curr_y = start_y
        self.curr_x = start_x
        self.level_sym = level_sym
        self.walkable = [self.level_sym["Floor"]]
        self.pushable = self.walkable[:]
        self.pushable.append(self.level_sym["Pit"])
        try:
            self.symbol = self.level_sym[self.__class__.__name__]
        except KeyError:
            raise Exception("Unexpected _Movable derived class: %s" %
                            self.__class__.__name__)

    def move(self, move_dir, univ, mode = None): 
        """The basic move method that derived classes call to move.
        
        The derived classes first call this method with mode _DRY_RUN. This
        shows what would be in the way if the move in direction move_dir were
        attempted, by returning the blocking Boulder object if present or
        otherwise returning the scenery symbol. The derived classes then do 
        processing to see if this is a legal move. If it is, this method is 
        called again with mode _DO_MOVE to do the move and return the scenery
        symbol for final processing such as filling in a pit.
        
        Input: 
        
        move_dir: a movement constant (UP, DOWN, LEFT, RIGHT) from module
            action.

        univ : Universe object holding current game state.

        mode: _DRY_RUN or _DO_MOVE (specified by derived classes). Note:
            though a default of None is given, the mode should always be
            explicitly passed by the derived class.
        
        Returns:
        
        if mode == _DRY_RUN:
            if a Boulder object is in the way, it returns the object.
            Otherwise, it returns the character from the level map for the
            target move location.
            
        if mode == _DO_MOVE:
            the character from the level map for the target move location. 
            (The _Movable's current location is updated.)
        
        """
        axis = _MOVE_TEST[move_dir]["axis"]
        change = _MOVE_TEST[move_dir]["change"]
        if axis == "y":
            target_y = self.curr_y + change
            target_x = self.curr_x
        elif axis == "x":
            target_y = self.curr_y
            target_x = self.curr_x + change
        else:
            raise Exception("Unexpected direction: %s" % str(axis))
        if mode == _DRY_RUN:
            for boulder in univ.boulders:
                if boulder.curr_y == target_y and boulder.curr_x == target_x:
                    return boulder
            return univ.level_map[target_y][target_x]
        elif mode == _DO_MOVE:
            self.curr_y = target_y
            self.curr_x = target_x
            return univ.level_map[self.curr_y][self.curr_x]
        else:
            raise Exception("Unexpected move mode: %s" % str(mode))

class Boulder(_Movable):
    
    """Class representing a boulder.
    
    Methods:
    
    move(move_dir, univ): Attempt to move boulder in direction move_dir.
        
    """

    def move(self, move_dir, univ):
        """Attempt to move boulder in direction move_dir.
        
        This method extends _Movable.move(...).
        
        Attempt to move Boulder in direction move_dir. The move is possible if
        the target square is a pushable (floor or pit). If the move is
        possible, move the Boulder. If the Boulder moves into a pit, change the
        pit into floor.
        
        Input:
        
        move_dir : A movement constant (UP, DOWN, LEFT, RIGHT) from module
            action.
            
        univ : Universe object holding current game state
        
        """
        mov = super(Boulder, self).move(move_dir, univ, _DRY_RUN)
        if mov in self.pushable:
            super(Boulder, self).move(move_dir, univ, _DO_MOVE)
            if mov == self.level_sym["Pit"]:
                univ.level_map[self.curr_y][self.curr_x] = \
                    self.level_sym["Floor"]
                univ.pits_remaining -= 1
            return mov

class Player(_Movable):
    
    """Class representing the player.
    
    Methods:
    
    move(move_dir, univ): Attempt to move player in direction move_dir.
    
    """

    def move(self, move_dir, univ):
        """Attempt to move player in direction move_dir.
        
        This method extends _Movable.move(...). 
        
        Attempt to move player in the direction represented by move_dir. The
        move is possible if 
        
        - there is no boulder in the way and the scenery is walkable (Floor),
        or
        - there is a boulder in the way, and the boulder's target square is 
            a pushable (floor or pit).
        
        If the move is possible, move the player and boulder (if applicable). 
        If the boulder fills in a pit, delete the boulder from the Universe.
        The Boulder object will change the pit into floor.
        
        Input:
        
        move_dir: a movement constant (UP, DOWN, LEFT, RIGHT) from module
            action.
            
        univ : Universe object holding current game state
        
        """
        player_move_result = super(Player, self).move(move_dir, univ,
                                                      _DRY_RUN)
        if player_move_result in self.walkable:
            super(Player, self).move(move_dir, univ, _DO_MOVE)
            univ.moves_taken += 1
        if isinstance(player_move_result, Boulder):
            boulder_move_sq = player_move_result.move(move_dir, univ)
            if boulder_move_sq in self.pushable:
                super(Player, self).move(move_dir, univ, _DO_MOVE)
                univ.moves_taken += 1
                if boulder_move_sq == self.level_sym["Pit"]:
                    univ.delete_boulder(player_move_result)
