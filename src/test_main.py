# Copyright 2016, Jeremy Nation <jeremy@jeremynation.me>
# Released under the GPLv3. See included LICENSE file.
import curses
import os
from unittest import TestCase

import levelloader
from . import main

TEST_LEVELS_DIR = 'test_levels'


class TestMain(TestCase):

    def test_fakename(self):
        with self.assertRaises(levelloader.LevelFileHandlingError):
            curses.wrapper(main, 'FAKENAME')

    def test_empty_file(self):
        with self.assertRaises(levelloader.MalformedLevelFileError):
            curses.wrapper(
                main,
                os.path.join(TEST_LEVELS_DIR, 'empty_file.dat'),
            )

    def test_blank_line(self):
        with self.assertRaises(levelloader.MalformedLevelFileError):
            curses.wrapper(
                main,
                os.path.join(TEST_LEVELS_DIR, 'blank_line.dat'),
            )

    def test_empty_level(self):
        with self.assertRaises(levelloader.MalformedLevelFileError):
            curses.wrapper(
                main,
                os.path.join(TEST_LEVELS_DIR, 'empty_level.dat'),
            )

    def test_unrecog_sym_type(self):
        with self.assertRaises(levelloader.MalformedLevelFileError):
            curses.wrapper(
                main,
                os.path.join(TEST_LEVELS_DIR, 'unrecog_sym_type.dat'),
            )

    def test_dup_sym_type(self):
        with self.assertRaises(levelloader.MalformedLevelFileError):
            curses.wrapper(
                main,
                os.path.join(TEST_LEVELS_DIR, 'dup_sym_type.dat'),
            )

    def test_dup_sym(self):
        with self.assertRaises(levelloader.MalformedLevelFileError):
            curses.wrapper(
                main,
                os.path.join(TEST_LEVELS_DIR, 'dup_sym.dat'),
            )

    def test_dup_level_names(self):
        with self.assertRaises(levelloader.MalformedLevelFileError):
            curses.wrapper(
                main,
                os.path.join(TEST_LEVELS_DIR, 'dup_level_names.dat'),
            )

    def test_no_level_names(self):
        with self.assertRaises(levelloader.MalformedLevelFileError):
            curses.wrapper(
                main,
                os.path.join(TEST_LEVELS_DIR, 'no_level_names.dat'),
            )

    def test_too_many_levels(self):
        with self.assertRaises(levelloader.MalformedLevelFileError):
            curses.wrapper(
                main,
                os.path.join(TEST_LEVELS_DIR, 'too_many_levels.dat'),
            )

    def test_no_player(self):
        with self.assertRaises(levelloader.MalformedLevelFileError):
            curses.wrapper(
                main,
                os.path.join(TEST_LEVELS_DIR, 'no_player.dat'),
            )

    def test_two_players(self):
        with self.assertRaises(levelloader.MalformedLevelFileError):
            curses.wrapper(
                main,
                os.path.join(TEST_LEVELS_DIR, 'two_players.dat'),
            )

    def test_no_pits(self):
        with self.assertRaises(levelloader.MalformedLevelFileError):
            curses.wrapper(
                main,
                os.path.join(TEST_LEVELS_DIR, 'no_pits.dat'),
            )

    def test_less_boulders_than_pits(self):
        with self.assertRaises(levelloader.MalformedLevelFileError):
            curses.wrapper(
                main,
                os.path.join(TEST_LEVELS_DIR, 'less_boulders_than_pits.dat'),
            )
