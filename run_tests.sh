#!/bin/bash
#
# Copyright 2016, Jeremy Nation <jeremy@jeremynation.me>
# Released under the GPLv3. See included LICENSE file.
#
# A short test script for Roguelike Sokoban.
# Requires nosetests. See: http://nose.readthedocs.io/en/latest
#
PROG="./rlsokoban.py -L"
TEST_LEVELS_DIR="src/test_levels"

nosetests -w ./src

echo
read -p 'Press <ENTER> to run game with a large level'
$PROG $TEST_LEVELS_DIR/huge_level.dat
read -p 'Press <ENTER> to run game with a level using different symbols'
$PROG $TEST_LEVELS_DIR/different_symbols.dat
