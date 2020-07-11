# Copyright 2020, Jeremy Nation <jeremy@jeremynation.me>
# Released under the GPLv3. See included LICENSE file.
import os
import unittest

from src.levelloader import (
    BlankLineError,
    DuplicateSymbolValuesError,
    EmptySymbolError,
    LevelLoader,
    MissingSymbolDefinitionError,
    MultiplePlayersError,
    NoPitsError,
    NoPlayerError,
    NotEnoughBouldersError,
    SymbolTooBigError,
)

TEST_LEVELS_DIR = os.path.join('test', 'test_levels')


class TestLevelLoader(unittest.TestCase):

    def test_blank_line(self):
        with self.assertRaises(BlankLineError):
            LevelLoader(
                os.path.join(TEST_LEVELS_DIR, 'blank_line.yml'),
            )

    def test_duplicate_symbol_values(self):
        with self.assertRaises(DuplicateSymbolValuesError):
            LevelLoader(
                os.path.join(TEST_LEVELS_DIR, 'duplicate_symbol_values.yml'),
            )

    def test_empty_symbol_error(self):
        with self.assertRaises(EmptySymbolError):
            LevelLoader(
                os.path.join(TEST_LEVELS_DIR, 'empty_symbol.yml'),
            )

    def test_missing_symbol_definition(self):
        with self.assertRaises(MissingSymbolDefinitionError):
            LevelLoader(
                os.path.join(TEST_LEVELS_DIR, 'missing_symbol_definition.yml'),
            )

    def test_multiple_players(self):
        with self.assertRaises(MultiplePlayersError):
            LevelLoader(
                os.path.join(TEST_LEVELS_DIR, 'multiple_players.yml'),
            )

    def test_no_pits(self):
        with self.assertRaises(NoPitsError):
            LevelLoader(
                os.path.join(TEST_LEVELS_DIR, 'no_pits.yml'),
            )

    def test_no_player(self):
        with self.assertRaises(NoPlayerError):
            LevelLoader(
                os.path.join(TEST_LEVELS_DIR, 'no_player.yml'),
            )

    def test_not_enough_boulders(self):
        with self.assertRaises(NotEnoughBouldersError):
            LevelLoader(
                os.path.join(TEST_LEVELS_DIR, 'not_enough_boulders.yml'),
            )

    def test_symbol_too_big(self):
        with self.assertRaises(SymbolTooBigError):
            LevelLoader(
                os.path.join(TEST_LEVELS_DIR, 'symbol_too_big.yml'),
            )
