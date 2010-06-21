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
Level loading module for Roguelike Sokoban.

This module handles all of processing on the level before it is handed to a
Universe object to set up the game.

Classes:

LevelLoader(object) : Loads level from the level file and prepares it for
    a Universe object.

MalformedLevelFileError(Exception) : Raised if a problem is found while
    processing the level file.
    
"""

import constants as const

__author__ = const.AUTHOR
__email__ = const.AUTHOR_EMAIL
__copyright__ = const.COPYRIGHT
__license__ = const.LICENSE
__version__ = const.VERSION

class MalformedLevelFileError(Exception):
    
    """Raised if a problem is found while processing the level file."""
    
    pass

class LevelLoader(object):
    
    """Loads level from the level file and prepares it for a Universe object.
    
    This class reads the levels and the user-specified level symbols from the
    level file specified by the user or taken by default. It prepares them as
    needed so a Universe object can set up the level. If there are multiple
    levels available in the level file, this class calls a Display object to
    ask the user which level they want to play.
    
    There are also many places where this class can raise an exception if
    problems are found with the level file.
    
    Methods:
    
    __init__(level_file_name) : Load and parse the level file specified.
    
    get_level(disp, name = None) : Determine level to play and return
        information related to it.
    
    """

    def __init__(self, level_file_name):
        """Load and parse the level file specified.
        
        Input:
        
        level_file_name : name of the level file the user wants to use.
        
        Raises:
        
        IOError : if 
            - level file cannot be opened
        
        MalformedLevelFileError : if
            - level file is empty
            - a blank line is found in the level file
            - an empty level is found in the level file
            - an unrecognized symbol type is found in the level file
            - a symbol type is defined more than once
            - a symbol is used for more than one symbol type
            - a level name is found more than once
            - no level names are found in the level file
        
        """
        self.level_file_name = level_file_name
        try:
            level_file = open(self.level_file_name)
        except IOError:
            reason = "could not open file \'%s\'." % self.level_file_name
            raise IOError(reason)
        raw_level_file_lines = level_file.readlines()
        if raw_level_file_lines == []:
            reason = "file \'%s\' is empty." % self.level_file_name
            raise MalformedLevelFileError(reason)
        temp_level_file_lines = []
        level_symbol_lines = []
        symbol_type_counter = 0
        for i, line in enumerate(raw_level_file_lines):
            if line.strip() == "":
                reason = "blank line found in file \'%s\'." % \
                        self.level_file_name
                raise MalformedLevelFileError(reason)
            elif line[0] == const.COMMENT:
                continue
            elif symbol_type_counter < len(const.LEVEL_SYMBOL_TYPES):
                symbol_type_counter += 1
                level_symbol_lines.append(line)
                continue
            elif line[0].isalpha():
                line = line[:const.MAX_LEVEL_NAME_LENGTH]
                try:
                    if raw_level_file_lines[i+1][0].isalpha():
                        raise MalformedLevelFileError
                except (IndexError, MalformedLevelFileError):
                    reason = "empty level \'%s\' found in file \'%s\'." % \
                            (line.strip(), self.level_file_name)
                    raise MalformedLevelFileError(reason)
                temp_level_file_lines.append(line.rstrip())
            else:
                temp_level_file_lines.append(line.rstrip())
        self.level_file_lines = temp_level_file_lines
        self.__set_level_symbols(level_symbol_lines)
        self.__set_level_names()
        
    def __set_level_symbols(self, level_symbol_lines):
        """Set dictionary of level symbols using lines parsed from level file.
        
        This method is called during LevelLoader.__init__(...).
        
        Input: 
        
        level_symbol_lines : list of lines with level symbols parsed out of
            the level file.
        
        Raises:
        
        MalformedLevelFileError: if
            - an unrecognized symbol type is found in the level file
            - a symbol type is defined more than once
            - a symbol is used for more than one symbol type
        
        """
        level_sym = {}
        for line in level_symbol_lines:
            name, symbol = line.split("=")
            name = name.strip()
            symbol = symbol.strip()
            if name not in const.LEVEL_SYMBOL_TYPES:
                reason = "unrecognized symbol type \'%s\' found in file "\
                        "\'%s\'. Recognized symbol types are: " % \
                        (name, self.level_file_name)
                for i, sym in enumerate(const.LEVEL_SYMBOL_TYPES):
                    reason += sym
                    if i != (len(const.LEVEL_SYMBOL_TYPES)-1):
                        reason += ", "
                    else:
                        reason += "."
                raise MalformedLevelFileError(reason)
            for key in level_sym:
                if name == key:
                    reason = "symbol type \'%s\' defined more than once in "\
                            "file \'%s\'." % (name, self.level_file_name)
                    raise MalformedLevelFileError(reason)
                if symbol == level_sym[key]:
                    reason = "symbol \'%s\' used for more than one symbol "\
                            "type in file \'%s\'." % (symbol, 
                                                      self.level_file_name)
                    raise MalformedLevelFileError(reason)
            level_sym[name] = symbol
        self.level_sym = level_sym

    def __set_level_names(self):
        """Set dictionary of level names.
        
        This method is called during LevelLoader.__init__(...).
        
        Raises:
        
        MalformedLevelFileError : if
            - a level name is found more than once
            - no level names are found in the level file
        
        """
        level_names = []
        for line in self.level_file_lines:
            if line[0].isalpha():
                if line in level_names:
                    reason = "duplicate level name \'%s\' found in file "\
                    "\'%s\'." % (line, self.level_file_name)
                    raise MalformedLevelFileError(reason)
                else:
                    level_names.append(line)
        if level_names == []:
            reason = "no level names found in file \'%s\'." %\
                    self.level_file_name
            raise MalformedLevelFileError(reason)
        self.level_names = level_names
        
    def get_level(self, disp, name = None):
        """Determine level to play and return information related to it.
        
        The returns for this method are intended to be fed directly into the
        initialization method for a Universe object.
        
        Input:
        
        disp : Display object for the game.
        
        name : name of the level to play. This defaults to None; it should only
            be not None if the user is restarting the current level.
            
        Returns:
        
        - name of chosen file.
        
        - list containing lists that each represent one row in the level. They
            will be broken up as list(string). All rows are padded out with
            spaces to the length of the longest row to make a rectangle, and a
            ring of spaces surrounds everything. The ring of spaces is
            necessary because the game won't know how to handle something
            moving into a location that is not on the map.
                    
        - dictionary of symbols for the level.
        
        Raises:
        
        MalformedLevelFileError : if
            - there is not exactly one player.
            - there is not at least one pit.
            - there are not at least as many boulders as pits.
        
        """
        # Finding the level name in self.level_names is a bit tricky because
        # name is .stripped() but the name we're looking for is not.
        if name is not None:
            for entry in self.level_names:
                if name == entry[:len(name)]:
                    chosen_level_name = entry
                    break
        else:
            chosen_level_name = disp.level_prompt(self.level_names, 
                                              self.level_file_name)
        choice_number = self.level_names.index(chosen_level_name)
        start = self.level_file_lines.index(chosen_level_name) + 1
        if (choice_number + 1) == len(self.level_names):
            end = len(self.level_file_lines)
        else:
            end = self.level_file_lines.index(self.level_names[choice_number
                                                               + 1])
        self.chosen_level_name = chosen_level_name.strip()
        self.chosen_level_lines = self.level_file_lines[start:end]
        self.__process_level_lines()
        self.__exception_if_level_unplayable()
        return self.chosen_level_name, self.chosen_level_lines, self.level_sym

    def __process_level_lines(self):
        """Do final processing on the level lines.
        
        This method splits the level lines as strings into lists, pads lines
        out to the length of the longest line with spaces to make a rectangle,
        and adds a ring of spaces around everything.
        
        """
        level = self.chosen_level_lines
        max_line_length = reduce(max, [len(line) for line in level])
        # Pad each line with spaces to the end of the longest line.
        for line_num, line in enumerate(level[:]):
            line = list(line)
            while len(line) < max_line_length:
                line.append(" ")
            level[line_num] = line
        # Add line of spaces to the beginning and end of level.
        blank_line = []
        while len(blank_line) < max_line_length:
            blank_line.append(" ")
        level.insert(0, blank_line)
        level.append(blank_line)
        # Add a space to the beginning and end of each line
        for row in level:
            row.insert(0, " ")
            row.append(" ")

    def __exception_if_level_unplayable(self):
        """Raise an exception if the level is not obviously playable.
        
        Raises:
        
        MalformedLevelFileError : if
            - there is not exactly one player.
            - there is not at least one pit.
            - there are not at least as many boulders as pits.

        """
        boulders = 0
        players = 0
        pits = 0
        for row in self.chosen_level_lines:
            for square in row:
                if square == self.level_sym["Boulder"]:
                    boulders += 1
                elif square == self.level_sym["Player"]:
                    players += 1
                elif square == self.level_sym["Pit"]:
                    pits += 1
        if players != 1:
            reason = "level \'%s\' in file \'%s\' does not have exactly one "\
                    "player \'%s\'." % (self.chosen_level_name,
                                        self.level_file_name,
                                        self.level_sym["Player"])
            raise MalformedLevelFileError(reason)
        if pits == 0:
            reason = "level \'%s\' in file \'%s\' has no pits \'%s\'." % \
                    (self.chosen_level_name, self.level_file_name,
                     self.level_sym["Pit"])
            raise MalformedLevelFileError(reason)
        if boulders < pits:
            reason = "level \'%s\' in file \'%s\' does not have enough "\
                    "boulders (%s) to fill the pits \'%s\'." % \
                    (self.chosen_level_name, self.level_file_name,
                     self.level_sym["Boulder"], self.level_sym["Pit"])
            raise MalformedLevelFileError(reason)