# Copyright 2021, Jeremy Nation <jeremy@jeremynation.me>
# Released under the GPLv3. See included LICENSE file.
from typing import Sequence, TypedDict

from src.constants import LevelFileConsts


class LevelStr(TypedDict):
    name: str
    map: str


LevelsStr = list[LevelStr]

Symbols = dict[str, str]

LevelInfo = tuple[str, Sequence[str], Symbols]


def _get_levels_from_file(level_file_name: str) -> tuple[Symbols, LevelsStr]:
    with open(level_file_name) as level_file:
        lines = level_file.readlines()

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
                first_part, second_part = line_split[0], ""
            else:
                first_part, second_part = line_split
            symbols[first_part] = second_part
        else:
            if line.startswith(LevelFileConsts.NAME_PREFIX):
                _, level_name = line.split(LevelFileConsts.DELIMITER)
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
            raise SymbolTooBigError("%s: '%s'" % (symbol_name, symbol_value))

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
    def __init__(self, level_file_name: str):
        self.level_file_name = level_file_name
        self.symbols, levels_str = _get_levels_from_file(level_file_name)
        _validate_level_data(self.symbols, levels_str)
        self.levels: dict[str, Sequence[str]] = {
            level["name"]: _create_level_array(level["map"]) for level in levels_str
        }

    def get_level(self, level_name: str) -> LevelInfo:
        return level_name, self.levels[level_name], self.symbols


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
