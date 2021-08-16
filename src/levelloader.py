"""
Copyright 2021, Jeremy Nation <jeremy@jeremynation.me>
Released under the GPLv3. See included LICENSE file.

"""
import curses
from pathlib import Path
from typing import Sequence, TypedDict

from src.util import GAME_NAME, QUIT, TERMINAL_TOO_SMALL_TEXT, UTF_8, LevelFileConsts


class LevelStr(TypedDict):
    name: str
    map: str


LevelsStr = list[LevelStr]

Symbols = dict[str, str]


def _get_levels_from_file(level_filename: Path) -> tuple[Symbols, LevelsStr]:
    with level_filename.open(encoding=UTF_8) as file:
        lines = file.readlines()

    symbols: Symbols = {}
    levels: LevelsStr = []
    in_maps = False
    for line in lines:
        line = line.rstrip()
        if line.startswith(LevelFileConsts.COMMENT_MARKER):
            continue

        if line == LevelFileConsts.MAPS_START:
            in_maps = True
            continue

        if not in_maps:
            line_split = line.split(LevelFileConsts.DELIMITER)
            if len(line_split) == 1:
                first_part, second_part = (
                    line_split[0].strip().rstrip(LevelFileConsts.DELIMITER),
                    "",
                )
            else:
                first_part, second_part = [part.strip() for part in line_split]
            symbols[first_part] = second_part
        else:
            if line.startswith(LevelFileConsts.NAME_PREFIX):
                level_name = line.split(LevelFileConsts.DELIMITER)[1].strip()
                levels.append({"name": level_name, "map": ""})
            else:
                if not levels[-1]["map"]:
                    levels[-1]["map"] = line
                else:
                    levels[-1]["map"] = "\n".join((levels[-1]["map"], line))

    return symbols, levels


def _validate_level_data(symbols: Symbols, levels: LevelsStr) -> None:
    for symbol_name, symbol_value in symbols.items():
        if len(symbol_value) < 1:
            raise EmptySymbolError(symbol_name)
        if len(symbol_value) > 1:
            raise SymbolTooBigError(
                "{name}: '{value}'".format(name=symbol_name, value=symbol_value)
            )

    for symbol_name in ("boulder", "floor", "pit", "player"):
        if symbol_name not in symbols:
            raise MissingSymbolDefinitionError(symbol_name)

    if len(set(symbols.values())) != len(symbols.values()):
        raise DuplicateSymbolValuesError

    level_names: list[str] = []
    for level in levels:
        level_names.append(level["name"])
        level_counts = {"boulder": 0, "player": 0, "pit": 0}

        if not level["map"]:
            raise EmptyMapError(level["name"])

        lines = level["map"].split("\n")
        for line in lines:
            if not line:
                raise BlankLineError(level["name"])
            for char in line:
                if char == symbols["boulder"]:
                    level_counts["boulder"] += 1
                elif char == symbols["player"]:
                    level_counts["player"] += 1
                elif char == symbols["pit"]:
                    level_counts["pit"] += 1

        if level_counts["player"] == 0:
            raise NoPlayerError(level["name"])

        if level_counts["player"] > 1:
            raise MultiplePlayersError(level["name"])

        if level_counts["pit"] == 0:
            raise NoPitsError(level["name"])

        if level_counts["boulder"] < level_counts["pit"]:
            raise NotEnoughBouldersError(level["name"])


def _create_level_array(level_string: str) -> Sequence[str]:
    lines = level_string.split("\n")
    max_line_length = max([len(line) for line in lines])
    lines = [line.ljust(max_line_length) for line in lines]

    lines.insert(0, "".ljust(max_line_length))
    lines.append("".ljust(max_line_length))

    lines = [" " + line for line in lines]
    lines = [line + " " for line in lines]

    return lines


class LevelLoader(object):
    def __init__(self, level_filename: Path):
        self.level_filename = level_filename
        self.symbols, levels_str = _get_levels_from_file(self.level_filename)
        _validate_level_data(self.symbols, levels_str)
        self.levels: dict[str, Sequence[str]] = {
            level["name"]: _create_level_array(level["map"]) for level in levels_str
        }

    def _draw_names(self, scrn: curses.window) -> int:
        """Paint all text for prompting other than the prompt line."""
        # Two header lines + blank + level list + blank + prompt
        min_height = 2 + 1 + len(self.levels) + 1 + 1
        if min_height > scrn.getmaxyx()[0]:
            raise Exception(TERMINAL_TOO_SMALL_TEXT)
        welcome = "Welcome to {name}".format(name=GAME_NAME)
        levels_found_header = "The following levels were found in {name}:".format(
            name=self.level_filename
        )
        scrn.clear()
        curses.endwin()
        curses.curs_set(0)
        scrn.refresh()
        scrn.addstr(0, 0, welcome)
        scrn.addstr(1, 0, levels_found_header)
        for i, level_name in enumerate(self.levels):
            scrn.addstr(i + 3, 0, str(i + 1) + ". " + level_name)
        # Write prompt here
        return scrn.getyx()[0] + 2

    def level_prompt(self, scrn: curses.window) -> str:
        """Prompt the user for the level to play from the available choices."""

        first_prompt = (
            "Enter the number of the level you want to play, or '{quit}' to "
            "quit: ".format(quit=QUIT)
        )
        invalid_input_prompt = (
            "Invalid choice, please enter the number of an available level, or "
            "'{quit}' to quit: ".format(quit=QUIT)
        )

        level_names = list(self.levels.keys())

        if len(level_names) == 1:
            chosen_level_name = level_names[0]
            return chosen_level_name

        prompt = first_prompt
        while True:
            prompt_y = self._draw_names(scrn)
            scrn.addstr(prompt_y, 0, prompt)
            curses.echo()
            curses.curs_set(1)
            # FIXME: Weird things happen if you resize the terminal while being
            # prompted for raw_choice. Various workarounds such as using getch
            # rather than getstr or redrawing the screen if curses.KEY_RESIZE
            # is found in raw_choice have not fixed everything.
            raw_choice_unknown = scrn.getstr()
            if isinstance(raw_choice_unknown, bytes):
                raw_choice = raw_choice_unknown.decode("utf-8").strip()
            else:
                raise Exception("unknown value from getstr")
            curses.curs_set(0)
            curses.noecho()
            if raw_choice == QUIT:
                raise KeyboardInterrupt
            else:
                try:
                    choice = int(raw_choice)
                    if choice in range(1, len(level_names) + 1):
                        break
                except ValueError:
                    pass
                prompt = invalid_input_prompt
        choice -= 1
        chosen_level_name = level_names[choice]
        return chosen_level_name.rstrip()


class BlankLineError(Exception):
    pass


class DuplicateSymbolValuesError(Exception):
    pass


class EmptyMapError(Exception):
    pass


class EmptySymbolError(Exception):
    pass


class MissingSymbolDefinitionError(Exception):
    pass


class MultiplePlayersError(Exception):
    pass


class NoPitsError(Exception):
    pass


class NoPlayerError(Exception):
    pass


class NotEnoughBouldersError(Exception):
    pass


class SymbolTooBigError(Exception):
    pass
