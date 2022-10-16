"""
Copyright Jeremy Nation <jeremy@jeremynation.me>.
Licensed under the GNU General Public License (GPL) v3.

"""
import unittest

from src.levelloader import LevelLoader
from src.util import TEST_LEVELS_DIR, RoguelikeSokobanError


class TestLevelLoader(unittest.TestCase):
    """Check for various level file problems."""

    def test_blank_line(self) -> None:
        """Error if a level map has a blank line."""
        with self.assertRaises(RoguelikeSokobanError) as context:
            LevelLoader(TEST_LEVELS_DIR / "blank_line.txt")
        self.assertEqual(
            "blank line in level: 'Blank Line Level'", str(context.exception)
        )

    def test_duplicate_symbol_values(self) -> None:
        """Error if a level file uses the same symbol value more than once."""
        with self.assertRaises(RoguelikeSokobanError) as context:
            LevelLoader(TEST_LEVELS_DIR / "duplicate_symbol_values.txt")
        self.assertEqual(
            "duplicate symbols in: 'boulder=0, floor=., pit=., player=@'",
            str(context.exception),
        )

    def test_empty_map_error(self) -> None:
        """Error if a level has an empty map."""
        with self.assertRaises(RoguelikeSokobanError) as context:
            LevelLoader(TEST_LEVELS_DIR / "empty_map.txt")
        self.assertEqual(
            "empty map for level: 'Empty Map Level'", str(context.exception)
        )

    def test_empty_symbol_error(self) -> None:
        """Error if a level file has an empty symbol."""
        with self.assertRaises(RoguelikeSokobanError) as context:
            LevelLoader(TEST_LEVELS_DIR / "empty_symbol.txt")
        self.assertEqual("empty symbol: 'boulder'", str(context.exception))

    def test_missing_symbol_definition(self) -> None:
        """Error if a level file is entirely missing a symbol definition."""
        with self.assertRaises(RoguelikeSokobanError) as context:
            LevelLoader(TEST_LEVELS_DIR / "missing_symbol_definition.txt")
        self.assertEqual("missing symbol definition: 'boulder'", str(context.exception))

    def test_multiple_players(self) -> None:
        """Error if a level map has multiple players."""
        with self.assertRaises(RoguelikeSokobanError) as context:
            LevelLoader(TEST_LEVELS_DIR / "multiple_players.txt")
        self.assertEqual(
            "multiple players in level: 'Multiple Players Level'",
            str(context.exception),
        )

    def test_no_pits(self) -> None:
        """Error if a level map has no pits."""
        with self.assertRaises(RoguelikeSokobanError) as context:
            LevelLoader(TEST_LEVELS_DIR / "no_pits.txt")
        self.assertEqual("no pits in level: 'No Pits Level'", str(context.exception))

    def test_no_player(self) -> None:
        """Error if a level map has no player."""
        with self.assertRaises(RoguelikeSokobanError) as context:
            LevelLoader(TEST_LEVELS_DIR / "no_player.txt")
        self.assertEqual(
            "no player in level: 'No Player Level'", str(context.exception)
        )

    def test_not_enough_boulders(self) -> None:
        """Error if a level map doesn't have enough boulders."""
        with self.assertRaises(RoguelikeSokobanError) as context:
            LevelLoader(TEST_LEVELS_DIR / "not_enough_boulders.txt")
        self.assertEqual(
            "not enough boulders in level: 'Not Enough Boulders Level'",
            str(context.exception),
        )

    def test_symbol_too_big(self) -> None:
        """Error if a symbol value is too big."""
        with self.assertRaises(RoguelikeSokobanError) as context:
            LevelLoader(TEST_LEVELS_DIR / "symbol_too_big.txt")
        self.assertEqual("symbol too big: 'boulder': '0.'", str(context.exception))
