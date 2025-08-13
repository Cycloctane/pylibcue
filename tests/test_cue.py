import unittest
from os.path import dirname, join

import pylibcue

TEST_DATA = join(dirname(__file__), "testdata")


class TestCue(unittest.TestCase):

    def test_example_cue(self):
        cd = pylibcue.Cd.from_path(join(TEST_DATA, "example.cue"))
        self.assertEqual(cd.cdtext.performer, "サンドリオン")
        self.assertEqual(cd.cdtext.title, "天体図")
        self.assertEqual(len(cd), 4)

        for i in cd:
            self.assertEqual(i.filename, "COCC-18150.wav")
            self.assertIs(i.mode, pylibcue.TrackMode.AUDIO)
            self.assertEqual(i.cdtext.performer, "サンドリオン")

        track_01 = cd[0]
        self.assertEqual(track_01.cdtext.title, "天体図")
        self.assertEqual(track_01.isrc, "JPCO02329890")
        self.assertEqual(track_01.start, (0, 0, 0))
        self.assertEqual(track_01.length, (4, 8, 50))
        self.assertEqual(track_01.zero_pre, (0, 0, 0))

        track_02 = cd[1]
        self.assertEqual(track_02.cdtext.title, "ゆびきりの唄")
        self.assertEqual(track_02.isrc, "JPCO02329840")
        self.assertEqual(track_02.start, (4, 10, 59))
        self.assertEqual(track_02.length, (4, 4, 32))
        self.assertEqual(track_02.zero_pre, (0, 2, 9))

        track_04 = cd[3]
        self.assertEqual(track_04.cdtext.title, "ゆびきりの唄 (off vocal ver.)")
        self.assertEqual(track_04.isrc, "JPCO02329849")
        self.assertEqual(track_04.start, (12, 27, 43))
        self.assertIs(track_04.length, None)
        self.assertEqual(track_04.zero_pre, (0, 2, 18))


if __name__ == "__main__":
    unittest.main()
