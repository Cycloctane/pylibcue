import unittest
from pathlib import Path

import pylibcue

TEST_CUE = Path(__file__).parent / "testdata" / "example.cue"


class TestParsing(unittest.TestCase):

    def test_from_str(self):
        with TEST_CUE.open("r", encoding='utf-8') as f:
            content = f.read()
        cd = pylibcue.Cd.from_str(content)
        self.assertEqual(cd.cdtext.title, "天体図")
        self.assertEqual(len(cd), 4)

    def test_from_file_text_mode(self):
        with TEST_CUE.open("r", encoding='utf-8') as f:
            cd = pylibcue.Cd.from_file(f)
            self.assertFalse(f.closed)
        self.assertEqual(cd.cdtext.title, "天体図")
        self.assertEqual(len(cd), 4)

    def test_from_file_binary_mode(self):
        with TEST_CUE.open("rb") as f:
            cd = pylibcue.Cd.from_file(f)
            self.assertFalse(f.closed)
        self.assertEqual(cd.cdtext.title, "天体図")

    def test_encoding(self):
        cd = pylibcue.Cd.from_path(TEST_CUE.parent / "example.jis.cue", encoding='shift-jis')
        self.assertEqual(cd.encoding, 'shift-jis')
        self.assertEqual(cd.cdtext.title, "天体図")
        self.assertEqual(cd[0].cdtext.title, "天体図")

    def test_error_unreadable(self):
        with self.assertRaises(IOError) as e, TEST_CUE.open("a") as f:
            _ = pylibcue.Cd.from_file(f)
        self.assertEqual(str(e.exception), "Failed to read file.")

    def test_error_parse(self):
        with self.assertRaises(ValueError) as e:
            _ = pylibcue.Cd.from_str("123456")
        self.assertEqual(str(e.exception), "Failed to parse cue string.")


if __name__ == "__main__":
    unittest.main()
