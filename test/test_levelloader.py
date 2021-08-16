"""
Copyright 2021, Jeremy Nation <jeremy@jeremynation.me>
Released under the GPLv3. See included LICENSE file.

"""
import unittest
from pathlib import Path

from src.levelloader import LevelLoader
from src.util import RoguelikeSokobanError

TEST_LEVELS_DIR = Path("test") / "test_levels"


class TestLevelLoader(unittest.TestCase):
    def test_blank_line(self) -> None:
        with self.assertRaises(RoguelikeSokobanError) as context:
            LevelLoader(TEST_LEVELS_DIR / "blank_line.txt")
        self.assertEqual(
            "blank line in level: 'Blank Line Level'", str(context.exception)
        )

    def test_duplicate_symbol_values(self) -> None:
        with self.assertRaises(RoguelikeSokobanError) as context:
            LevelLoader(TEST_LEVELS_DIR / "duplicate_symbol_values.txt")
        self.assertEqual(
            "duplicate symbols in: 'boulder=0, floor=., pit=., player=@'",
            str(context.exception),
        )

    def test_empty_map_error(self) -> None:
        with self.assertRaises(RoguelikeSokobanError) as context:
            LevelLoader(TEST_LEVELS_DIR / "empty_map.txt")
        self.assertEqual(
            "empty map for level: 'Empty Map Level'", str(context.exception)
        )

    def test_empty_symbol_error(self) -> None:
        with self.assertRaises(RoguelikeSokobanError) as context:
            LevelLoader(TEST_LEVELS_DIR / "empty_symbol.txt")
        self.assertEqual("empty symbol: 'boulder'", str(context.exception))

    def test_missing_symbol_definition(self) -> None:
        with self.assertRaises(RoguelikeSokobanError) as context:
            LevelLoader(TEST_LEVELS_DIR / "missing_symbol_definition.txt")
        self.assertEqual("missing symbol definition: 'boulder'", str(context.exception))

    def test_multiple_players(self) -> None:
        with self.assertRaises(RoguelikeSokobanError) as context:
            LevelLoader(TEST_LEVELS_DIR / "multiple_players.txt")
        self.assertEqual(
            "multiple players in level: 'Multiple Players Level'",
            str(context.exception),
        )

    def test_no_pits(self) -> None:
        with self.assertRaises(RoguelikeSokobanError) as context:
            LevelLoader(TEST_LEVELS_DIR / "no_pits.txt")
        self.assertEqual("no pits in level: 'No Pits Level'", str(context.exception))

    def test_no_player(self) -> None:
        with self.assertRaises(RoguelikeSokobanError) as context:
            LevelLoader(TEST_LEVELS_DIR / "no_player.txt")
        self.assertEqual(
            "no player in level: 'No Player Level'", str(context.exception)
        )

    def test_not_enough_boulders(self) -> None:
        with self.assertRaises(RoguelikeSokobanError) as context:
            LevelLoader(TEST_LEVELS_DIR / "not_enough_boulders.txt")
        self.assertEqual(
            "not enough boulders in level: 'Not Enough Boulders Level'",
            str(context.exception),
        )

    def test_symbol_too_big(self) -> None:
        with self.assertRaises(RoguelikeSokobanError) as context:
            LevelLoader(TEST_LEVELS_DIR / "symbol_too_big.txt")
        self.assertEqual("symbol too big: 'boulder': '0.'", str(context.exception))
