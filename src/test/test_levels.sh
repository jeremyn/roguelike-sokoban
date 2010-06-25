#!/bin/bash
#
# A short test script for Roguelike Sokoban.
#
# This script first tries to start the game with various malformed levels so
# the person running the script can verify that the correct error is reported.
# Then, the script plays working levels that test different parts of the game.
#
# This should eventually be replaced with a more comprehensive and automated
# testing process.

PROG="../../rlsokoban.py -L"

echo "Running rlsokoban.py with bad level files."
echo "These should all report an error:"
echo
$PROG FAKENAME
$PROG empty_file.dat
$PROG blank_line.dat
$PROG empty_level.dat
$PROG unrecog_sym_type.dat
$PROG dup_sym_type.dat
$PROG dup_sym.dat
$PROG dup_level_names.dat
$PROG no_level_names.dat
$PROG too_many_levels.dat
$PROG no_player.dat
$PROG two_players.dat
$PROG no_pits.dat
$PROG less_boulders_than_pits.dat
echo
echo "Now running rlsokoban.py with good level files."
echo
read -p 'Press <ENTER> to run game with a large level'
$PROG huge_level.dat
read -p 'Press <ENTER> to run game with a level using different symbols'
$PROG different_symbols.dat
