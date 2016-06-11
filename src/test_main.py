# Copyright 2016, Jeremy Nation <jeremy@jeremynation.me>
# Released under the GPLv3. See included LICENSE file.
import curses
import os
from unittest import TestCase

import levelloader
from . import main

TEST_LEVELS_DIR = 'test_levels'


class TestMain(TestCase):

    def test_blank_line(self):
        with self.assertRaises(levelloader.BlankLineError):
            curses.wrapper(
                main,
                os.path.join(TEST_LEVELS_DIR, 'blank_line.yml'),
            )

    def test_duplicate_symbol_values(self):
        with self.assertRaises(levelloader.DuplicateSymbolValuesError):
            curses.wrapper(
                main,
                os.path.join(TEST_LEVELS_DIR, 'duplicate_symbol_values.yml'),
            )

    def test_empty_symbol_error(self):
        with self.assertRaises(levelloader.EmptySymbolError):
            curses.wrapper(
                main,
                os.path.join(TEST_LEVELS_DIR, 'empty_symbol.yml'),
            )

    def test_missing_symbol_definition(self):
        with self.assertRaises(levelloader.MissingSymbolDefinitionError):
            curses.wrapper(
                main,
                os.path.join(TEST_LEVELS_DIR, 'missing_symbol_definition.yml'),
            )

    def test_multiple_players(self):
        with self.assertRaises(levelloader.MultiplePlayersError):
            curses.wrapper(
                main,
                os.path.join(TEST_LEVELS_DIR, 'multiple_players.yml'),
            )

    def test_no_pits(self):
        with self.assertRaises(levelloader.NoPitsError):
            curses.wrapper(
                main,
                os.path.join(TEST_LEVELS_DIR, 'no_pits.yml'),
            )

    def test_no_player(self):
        with self.assertRaises(levelloader.NoPlayerError):
            curses.wrapper(
                main,
                os.path.join(TEST_LEVELS_DIR, 'no_player.yml'),
            )

    def test_not_enough_boulders(self):
        with self.assertRaises(levelloader.NotEnoughBouldersError):
            curses.wrapper(
                main,
                os.path.join(TEST_LEVELS_DIR, 'not_enough_boulders.yml'),
            )

    def test_symbol_too_big(self):
        with self.assertRaises(levelloader.SymbolTooBigError):
            curses.wrapper(
                main,
                os.path.join(TEST_LEVELS_DIR, 'symbol_too_big.yml'),
            )
