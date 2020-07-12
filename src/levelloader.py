# Copyright 2020, Jeremy Nation <jeremy@jeremynation.me>
# Released under the GPLv3. See included LICENSE file.
from src.constants import LevelFileConsts


def _get_levels_from_file(level_file_name):
    with open(level_file_name) as level_file:
        lines = level_file.readlines()

    symbols = {}
    levels = []
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
                first_part, second_part = line_split[0], ''
            else:
                first_part, second_part = line_split
            symbols[first_part] = second_part
        else:
            if line.startswith(LevelFileConsts.NAME_PREFIX):
                _, level_name = line.split(LevelFileConsts.DELIMITER)
                levels.append({
                    'name': level_name,
                    'map': None
                })
            else:
                if levels[-1]['map'] is None:
                    levels[-1]['map'] = line
                else:
                    levels[-1]['map'] = '\n'.join((levels[-1]['map'], line))

    return {
        'symbols': symbols,
        'levels': levels,
    }


def _validate_level_data(symbols, levels):
    for symbol_name, symbol_value in symbols.items():
        if len(symbol_value) < 1:
            raise EmptySymbolError(symbol_name)
        if len(symbol_value) > 1:
            raise SymbolTooBigError("%s: '%s'" % (symbol_name, symbol_value))

    for symbol_name in ('boulder', 'floor', 'pit', 'player'):
        if symbol_name not in symbols:
            raise MissingSymbolDefinitionError(symbol_name)

    if len(set(symbols.values())) != len(symbols.values()):
        raise DuplicateSymbolValuesError

    level_names = []
    for level in levels:
        level_names.append(level['name'])
        level_counts = {
            'boulder': 0,
            'player': 0,
            'pit': 0,
        }
        lines = level['map'].split('\n')
        for line in lines:
            if not line:
                raise BlankLineError(level['name'])
            for char in line:
                if char == symbols['boulder']:
                    level_counts['boulder'] += 1
                elif char == symbols['player']:
                    level_counts['player'] += 1
                elif char == symbols['pit']:
                    level_counts['pit'] += 1

        if level_counts['player'] == 0:
            raise NoPlayerError(level['name'])

        if level_counts['player'] > 1:
            raise MultiplePlayersError(level['name'])

        if level_counts['pit'] == 0:
            raise NoPitsError(level['name'])

        if level_counts['boulder'] < level_counts['pit']:
            raise NotEnoughBouldersError(level['name'])


def _create_level_array(level_string):
    lines = level_string.split('\n')
    max_line_length = max([len(line) for line in lines])
    lines = [line.ljust(max_line_length) for line in lines]

    lines.insert(0, ''.ljust(max_line_length))
    lines.append(''.ljust(max_line_length))

    lines = [' ' + line for line in lines]
    lines = [line + ' ' for line in lines]

    return lines


class LevelLoader(object):

    def __init__(self, level_file_name):
        self.level_file_name = level_file_name
        file_data = _get_levels_from_file(level_file_name)
        self.symbols = file_data['symbols']
        self.levels = file_data['levels']
        _validate_level_data(self.symbols, self.levels)
        self.levels = [
            {
                'name': level['name'],
                'map': _create_level_array(level['map']),
            }
            for level in self.levels
        ]

    def get_level(self, disp, level_name=None):
        if level_name is None:
            level_name = disp.level_prompt(
                [level['name'] for level in self.levels],
                self.level_file_name,
            )

        for level in self.levels:
            if level['name'] == level_name:
                level_lines = level['map']
                break

        level_name = level_name.rstrip()

        return level_name, level_lines, self.symbols


class BlankLineError(Exception):
    pass


class DuplicateSymbolValuesError(Exception):
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
