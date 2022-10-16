"""
Copyright Jeremy Nation <jeremy@jeremynation.me>.
Licensed under the GNU General Public License (GPL) v3.

"""
import filecmp
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from convert_xsokoban import get_level_groups, get_parser, main
from src.util import TEST_DIR

CONVERTED_LEVELS_DIR = Path("levels")
SRC_LEVELS_DIR = TEST_DIR / "xsokoban_src"

CONVERTED_FILENAME_STR = "xsokoban1-10.txt"


class TestConvertXSokoban(unittest.TestCase):
    """Test convert_sokoban.py."""

    def test_get_level_groups(self) -> None:
        """Test get_level_groups."""
        self.assertEqual([(1, 7)], get_level_groups(7))
        self.assertEqual([(1, 10)], get_level_groups(10))
        self.assertEqual([(1, 10), (11, 20)], get_level_groups(20))
        self.assertEqual([(1, 10), (11, 20), (21, 23)], get_level_groups(23))

    def test_main(self) -> None:
        """Test main."""
        with TemporaryDirectory() as output_dir_str:
            parser = get_parser()
            inputs = [
                "--output-dir",
                output_dir_str,
                "--max-level",
                str(10),
                str(SRC_LEVELS_DIR),
            ]
            args = parser.parse_args(inputs)
            output_dir = Path(output_dir_str)
            self.assertEqual(
                {
                    "input_dir": SRC_LEVELS_DIR,
                    "max_level": 10,
                    "output_dir": output_dir,
                },
                vars(args),
            )

            main(args)
            self.assertTrue(
                filecmp.cmp(
                    CONVERTED_LEVELS_DIR / CONVERTED_FILENAME_STR,
                    output_dir / CONVERTED_FILENAME_STR,
                )
            )
