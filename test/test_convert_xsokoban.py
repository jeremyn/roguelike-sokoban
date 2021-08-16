"""
Copyright 2021, Jeremy Nation <jeremy@jeremynation.me>
Released under the GPLv3. See included LICENSE file.

"""
import filecmp
import os
import unittest
from tempfile import TemporaryDirectory

from convert_xsokoban import get_level_groups, get_parser, main

TEST_LEVELS_DIR = os.path.join("test", "xsokoban_src")
VALID_LEVELS_DIR = "levels"

VALID_FILENAME = "xsokoban1-10.txt"


class TestConvertXSokoban(unittest.TestCase):
    def test_get_level_groups(self) -> None:
        self.assertEqual([(1, 7)], get_level_groups(7))
        self.assertEqual([(1, 10)], get_level_groups(10))
        self.assertEqual([(1, 10), (11, 20)], get_level_groups(20))
        self.assertEqual([(1, 10), (11, 20), (21, 23)], get_level_groups(23))

    def test_main(self) -> None:
        with TemporaryDirectory() as output_dir:
            parser = get_parser()
            inputs = [
                "--output-dir",
                output_dir,
                "--max-level",
                str(10),
                str(TEST_LEVELS_DIR),
            ]
            args = parser.parse_args(inputs)
            self.assertEqual(
                {
                    "input_dir": TEST_LEVELS_DIR,
                    "max_level": 10,
                    "output_dir": output_dir,
                },
                vars(args),
            )

            main(args)
            self.assertTrue(
                filecmp.cmp(
                    os.path.join(VALID_LEVELS_DIR, VALID_FILENAME),
                    os.path.join(output_dir, VALID_FILENAME),
                )
            )
