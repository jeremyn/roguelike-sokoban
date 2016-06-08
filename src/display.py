# Copyright 2016, Jeremy Nation <jeremy@jeremynation.me>
# Released under the GPLv3. See included LICENSE file.
"""
Display module for Roguelike Sokoban.

This module manages most of the user interface. Roguelike Sokoban uses the
curses library for user interaction.

Classes:

Display(object) : Main display class used by the rest of Roguelike Sokoban.

WindowTooSmallError(Exception) : Raised if the terminal is too small for a
    minimal display.

"""

import curses
import constants as const
import action

__author__ = const.AUTHOR
__email__ = const.AUTHOR_EMAIL
__copyright__ = const.COPYRIGHT
__license__ = const.LICENSE
__version__ = const.VERSION

class WindowTooSmallError(Exception):
    
    """Raised if the terminal is too small for a minimal display."""
    
    pass

class _Coordinates(object):
    
    """Container class for all the coordinates used by Display.
    
    Data
    ----
    min_y, min_x : min, max row of main screen
    max_y, max_x : min, max column of main screen
    mid_y, mid_x : mid row, column of main screen
    level_height : rows in level
    level_width : columns in level
    self.levelpad_coords : coordinates needed for levelpad.noutrefresh(...)
    self.scroll_info : dictionary used by Display.set_scroll_line(...)
    
    """
    
    def __init__(self, scrn, lines, univ):
        """Initialize Coordinates.
        
        Input:
        
        scrn : curses main window object
        lines : return value from Display.__return_lines(...)
        univ : Universe object holding current game state
        
        Raises:
        
        WindowTooSmallError : if terminal is too small to display a minimal
            view
        
        """
        self.min_y, self.min_x = scrn.getbegyx()
        self.max_y, self.max_x = scrn.getmaxyx()
        self.mid_y = (self.max_y + self.min_y) / 2
        self.mid_x = (self.max_x + self.min_x) / 2
        self.level_height = len(univ.level_map)
        self.level_width = len(univ.level_map[0])
        self.levelpad_coords, self.scroll_info = \
                self.__find_levelpad_coords(lines, univ)
        self.__exception_if_too_small(lines)
    
    def __exception_if_too_small(self, lines):
        """Raise an exception if the terminal is not large enough.
        
        Input:
        
        lines : return value from Display.__return_lines(...)
        
        Raises:
        
        WindowTooSmallError : if terminal is too small to display a minimal
            view
            
        """
        padding_for_level_view = 7
        extracted_lines = lines["top"] + lines["bottom"]        
        min_height = len(extracted_lines) + padding_for_level_view
        min_width = reduce(max, [len(line) for line in extracted_lines])
        if self.max_y < min_height or self.max_x < min_width:
            raise WindowTooSmallError
    
    def __find_levelpad_coords(self, lines, univ):
        """Calculate coordinates to display levelpad in available space.
        
        Input:
        
        lines : return value from Display.__return_lines(...)
        
        univ : Universe object holding current game state
        
        Returns:
        
        - 6-tuple holding input coordinates to 
            Display.levelpad.noutrefresh(...)
        - dictionary holding True/False state about scrolling up, down, left
            and right
            
        """
        avail_min_y = self.min_y + len(lines["top"]) + 1
        avail_max_y = self.max_y - len(lines["bottom"]) - 2
        avail_min_x = self.min_x + 1
        avail_max_x = self.max_x - 2
        avail_y = avail_max_y - avail_min_y
        avail_x = avail_max_x - avail_min_x
        # Make avail_y and avail_x always even to prevent glitching due to 
        # division by 2.
        if avail_y % 2 != 0: 
            avail_y -= 1
        if avail_x % 2 != 0:
            avail_x -= 1
        avail_mid_y = (avail_max_y + avail_min_y) / 2
        # +1 in avail_mid_x centers the map better.
        avail_mid_x = (avail_max_x + avail_min_x) / 2 + 1
        
        # Place the levelpad in the available space in the middle of the
        # screen. If the levelpad is bigger than the available space, then
        # scroll within the pad appropriately.
        player_y = univ.player.curr_y
        player_x = univ.player.curr_x
        
        if avail_y >= self.level_height:
            pminy = 0
            sminy = avail_mid_y - (self.level_height / 2)
            smaxy = avail_mid_y + (self.level_height / 2)
        else:
            if (self.level_height - player_y) < (avail_y / 2):
                pminy = self.level_height - avail_y
            else:
                pminy = player_y - (avail_y / 2)
            sminy = avail_min_y
            smaxy = avail_max_y

        if avail_x >= self.level_width:
            pminx = 0
            sminx = avail_mid_x - (self.level_width / 2)
            smaxx = avail_mid_x + (self.level_width / 2)
        else:
            if (self.level_width - player_x) < (avail_x / 2):
                pminx = self.level_width - avail_x
            else:
                pminx = player_x - (avail_x / 2)
            sminx = avail_min_x
            smaxx = avail_max_x
            
        # Construct and return a scroll information dictionary to later use to
        # make an information line about which way(s) the level scrolls off the
        # terminal.
        scroll = {}
        scroll["UP"] = pminy > 0
        scroll["DOWN"] = (self.level_height > avail_y and
                          pminy < self.level_height - avail_y)
        scroll["LEFT"] = pminx > 0
        scroll["RIGHT"] = (self.level_width > avail_x and
                           pminx < self.level_width - avail_x)
        
        return (pminy, pminx, sminy, sminx, smaxy, smaxx), scroll
        
class Display(object):
    
    """Main display class used by the rest of Roguelike Sokoban.
    
    Main display class that displays the current state of the game on the map
    in the available space, along with various static and status text. Also 
    handles display for prompting user to choose a level to play.
    
    Methods:

    __init__(scrn) : Initialize display with curses main window scrn.
    
    level_init(univ) : Prepare Display to display level contained in Universe
        object univ.
        
    draw(univ) : Draw the screen using the level information in Universe object
        univ.
        
    level_prompt(level_names, level_file_name) : Prompt the user for the level
        to play from the available choices.
        
    get_action() : Get action from user.
    
    """

    def __init__(self, scrn):
        """Initialize display with curses main window scrn.
        
        Input:
        
        scrn : main window returned by curses.wrapper(...).
        
        """
        self.scrn = scrn

    def level_init(self, univ, high_score):
        """Prepare Display to display level contained in Universe object univ.
        
        This method should be called after a level has been loaded into a 
        Universe object but before Display is called to display the game state.
        
        Input: 
        
        univ : Universe object holding current game state.
        
        high_score : integer of current high score for level.
        
        """
        self.levelpad = curses.newpad(len(univ.level_map)+1, 
                                      len(univ.level_map[0])+1)
        self.level_sym = univ.level_sym
        self.text = {
                     "game_name": "%s, v%s" % (const.GAME_NAME, const.VERSION), 
                     "bug_line": "Comments welcome: " + const.ISSUE_TRACKER,
                     "instructions1": "Use the arrow keys to move around, "\
                            "\'%s\' to quit, and \'%s\' to restart this "\
                            "level." % (const.QUIT, const.PLAY_AGAIN),
                    "instructions2": "Move yourself (%s) over floor (%s) "\
                            "into boulders (%s) to push them into pits "\
                            "(%s)." % (
                                       self.level_sym["Player"],
                                       self.level_sym["Floor"],
                                       self.level_sym["Boulder"],
                                       self.level_sym["Pit"],
                                       ),
                    "level_name": "Level: %s" % univ.level_name,
                    "blank": "      ",
                    # scroll_info_line here is just a max sized placeholder.
                    # scroll_info_line is set in __set_scroll_line(...).
                    "scroll_info_line": "Scroll: UP, DOWN, LEFT, RIGHT",
                    "goal": "Fill every pit to solve the puzzle.",
                    "play_again_prompt": "-- Press \'%s\' to play again --" % \
                            const.PLAY_AGAIN,
                    "quit_prompt": "-- Press \'%s\' to quit --" % const.QUIT,
                    }
        self.high_score = high_score

    def __return_lines(self, univ):
        """Returns text lines based on current game state.
        
        Input:
        
        univ : Universe object holding current game state.
        
        Returns:
        
        - dictionary 'lines' of text lines used by other methods in this
            module.
        
        """
        self.text["status_pits"] = "Pits remaining: %d" % univ.pits_remaining
        self.text["status_moves"] = "Moves used: %d" % univ.moves_taken
        self.text["status_boulders"] = "Boulders remaining: %d" % \
                len(univ.boulders)
        self.text["congratulations"] = "You solved the puzzle in %d move%s! "\
                "Congratulations! " % (
                                       univ.moves_taken,
                                       (univ.moves_taken > 1) and "s" or "",
                                       )
        if self.high_score == const.NO_SCORE_SET:
            self.text["high_score"] = "No current best score"
            self.text["compared_to_high_score"] = "You set the first best "\
                    "score of %d moves!" % univ.moves_taken
        else:
            self.text["high_score"] = "Current best score: %d" % \
                    self.high_score
            if univ.moves_taken < self.high_score:
                self.text["compared_to_high_score"] = "You beat the current "\
                        "best score of %d moves!" % self.high_score
            else:
                self.text["compared_to_high_score"] = ""
        
        if not univ.game_won:
            lines = {
                     "top":    [
                                 self.text["game_name"],
                                 self.text["instructions1"],
                                 self.text["instructions2"],
                                 self.text["goal"],
                                 self.text["level_name"],
                                 ],
                     "bottom": [
                                 self.text["scroll_info_line"],
                                 self.text["status_pits"] + \
                                     self.text["blank"] + \
                                     self.text["status_boulders"] + \
                                     self.text["blank"] + \
                                     self.text["status_moves"],
                                 self.text["high_score"],
                                 self.text["bug_line"],
                                 ],
                     }
        else:
            lines = {
                     "top":    [
                                self.text["game_name"],
                                self.text["congratulations"],
                                self.text["compared_to_high_score"],
                                self.text["blank"],
                                self.text["level_name"],
                                ],
                     "bottom": [
                                self.text["blank"],
                                self.text["play_again_prompt"],
                                self.text["quit_prompt"],
                                self.text["bug_line"],
                                ]
                     }
        return lines    
    
    def __set_scroll_line(self, scroll_info):
        """Sets value for text line with scrolling information.
        
        Input:
        
        scroll_info : dictionary created by 
            Coordinates.__find_levelpad_coords(...). 
        
        """
        scroll_info_line = "Scroll: "
        for direction in ("UP", "DOWN", "LEFT", "RIGHT"):
            if scroll_info[direction]:
                scroll_info_line += direction + ", "
        if scroll_info_line == "Scroll: ":
            scroll_info_line = ""
        else:
            scroll_info_line = scroll_info_line[:-2]
        self.text["scroll_info_line"] = scroll_info_line
        
    def __paint_line(self, row, line):
        """Paint text line on main curses window centered horizontally.
        
        This method paints character by character, so curses will crash if 
        there is not enough horizontal space on which to paint.
        
        Also, this method will look for the symbol representing the player,
        for example '@', and paint it with curses attribute curses.A_REVERSE 
        to be consistent with __paint_levelpad(...).
        
        Input:
        
        row : integer specifying the row on which to paint the line.
        
        line : string to paint.
        
        """
        t_min_x = self.coords.mid_x - (len(line)/2)
        for i, char in enumerate(line):
            if line == self.text["instructions2"] and \
                    char == self.level_sym["Player"]:
                self.scrn.addch(row, t_min_x+i, char, curses.A_REVERSE)
            else:
                self.scrn.addch(row, t_min_x+i, char)
                
    def __paint_text_lines(self, lines):
        """Paint all text lines in lines onto main window.
        
        Input :
        
        lines: return value from Display.__return_lines(...).
        
        """
        for line_number, line in enumerate(lines["top"]):
            self.__paint_line(self.coords.min_y + line_number, line)
        for line_number, line in enumerate(lines["bottom"]):
            self.__paint_line(self.coords.max_y - len(lines["bottom"]) + \
                            line_number, line)  

    def __paint_levelpad(self, univ):
        """Paint the level map onto the levelpad created by level_init(...).
        
        Input:
        
        univ : Universe object holding current game state.
        
        """
        # Paint the level map onto levelpad.
        for row_index, row in enumerate(univ.level_map):
            for col_index, square in enumerate(row):
                self.levelpad.addch(row_index, col_index, square)
        # Paint the player onto levelpad.
        player_y = univ.player.curr_y
        player_x = univ.player.curr_x
        player_sym = univ.player.symbol
        self.levelpad.addch(player_y, player_x, player_sym, curses.A_REVERSE)
        # Paint the boulders onto levelpad.
        for boulder in univ.boulders:
            b_y, b_x, b_sym = boulder.curr_y, boulder.curr_x, boulder.symbol
            self.levelpad.addch(b_y, b_x, b_sym)

    def draw(self, univ):
        """Draw the screen using the level information in Universe object univ.
        
        Input:
        
        univ : Universe object holding current game state.
        
        Raises:
        
        WindowTooSmallError : if the terminal is too small to display a minimal
            view of the level.
        """
        self.scrn.clear()
        lines = self.__return_lines(univ)
        self.coords = _Coordinates(self.scrn, lines, univ)
        self.__set_scroll_line(self.coords.scroll_info)
        lines = self.__return_lines(univ)        
        self.__paint_text_lines(lines)
        self.scrn.noutrefresh()
        self.__paint_levelpad(univ)
        pminy, pminx, sminy, sminx, smaxy, smaxx = self.coords.levelpad_coords
        self.levelpad.noutrefresh(pminy, pminx, sminy, sminx, smaxy, smaxx)
        curses.doupdate()
        curses.curs_set(0)

    def level_prompt(self, level_names, level_file_name):
        """Prompt the user for the level to play from the available choices.
        
        If there is only one level name to choose from, this is returned
        without prompting the user.
        
        Input:
        
        level_names : list of possible level names from level_file_name
        level_file_name : name of the level file.
        
        Returns:
        
        - name of level chosen.
        
        Raises:
            
        WindowTooSmallError : if terminal is not tall enough to display
            properly.

        """

        def __draw_names():
            """Paint all text for prompting other than the prompt line.
            
            Raises:
            
            WindowTooSmallError : if terminal is not tall enough to display
                properly.
            
            """
            # Two header lines + blank + level list + blank + prompt
            min_height = 2 + 1 + len(level_names) + 1 + 1
            if min_height > self.scrn.getmaxyx()[0]:
                raise WindowTooSmallError 
            welcome = "Welcome to %s, v%s" % (const.GAME_NAME, const.VERSION)
            levels_found_header = "The following levels were found in %s:" % \
                    level_file_name
            self.scrn.clear()
            curses.endwin()
            curses.curs_set(0)
            self.scrn.refresh()
            self.scrn.addstr(0, 0, welcome)
            self.scrn.addstr(1, 0, levels_found_header)
            for i, level_name in enumerate(level_names):
                self.scrn.addstr(i+3, 0, str(i+1) + ". " + level_name)
            return self.scrn.getyx()[0] + 2 # Write prompt here

        # Start level_prompt main body.
        first_prompt = "Enter the number of the level you want to play, " \
                "or \'%s\' to quit: " % const.QUIT
        invalid_input_prompt = "Invalid choice, please enter the number of "\
                "an available level, or \'%s\' to quit: " % const.QUIT

        # If only one level available, return it.
        if len(level_names) == 1:
            chosen_level_name = level_names[0]
            return chosen_level_name

        # Otherwise, prompt user to choose.
        prompt = first_prompt
        while True:
            prompt_y = __draw_names()
            self.scrn.addstr(prompt_y, 0, prompt)
            curses.echo()
            curses.curs_set(1)
            # FIXME: Weird things happen if you resize the terminal while being
            # prompted for raw_choice. Various workarounds such as using getch
            # rather than getstr or redrawing the screen if curses.KEY_RESIZE
            # is found in raw_choice have not fixed everything.
            raw_choice = self.scrn.getstr()
            raw_choice = ("".join(raw_choice)).strip()
            curses.curs_set(0)
            curses.noecho()
            if raw_choice == const.QUIT:
                raise KeyboardInterrupt
            else:
                try:
                    choice = int(raw_choice)
                    if choice in range(1, len(level_names)+1):
                        break
                except ValueError:
                    pass
                prompt = invalid_input_prompt
        choice -= 1
        chosen_level_name = level_names[choice]
        return chosen_level_name

    def get_action(self):
        """Get action from user.
        
        Returns:
        
        - one of the constant values from module action.
        
        """
        k = self.scrn.getch()
        if k == curses.KEY_RESIZE:
            self.scrn.clear()
            curses.endwin()
            self.scrn.refresh()
            act = action.OTHER
        if k == curses.KEY_UP:
            act = action.UP
        elif k == curses.KEY_DOWN:
            act = action.DOWN
        elif k == curses.KEY_LEFT:
            act = action.LEFT
        elif k == curses.KEY_RIGHT:
            act = action.RIGHT
        elif k == ord(const.QUIT):
            act = action.QUIT
        elif k == ord(const.PLAY_AGAIN):
            act = action.PLAY_AGAIN
        else:
            act = action.OTHER
        return act
