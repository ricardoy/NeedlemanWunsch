import numpy as np
import unittest

from NeedlemanWunsch import NeedlemanWunsch


class EditDistance(NeedlemanWunsch):

    def score(self, a, b):
        if a == b:
            return 1
        else:
            return -1

    def retrieve_position(self, v, i):
        return v[i]

    def size(self, v):
        return len(v)


class NeedlemanWunschTest(unittest.TestCase):

    def test_match(self):
        ed = EditDistance(np.int32, -1)
        r = ed.distance('a', 'a')
        self.assertEqual(1, r.score)
        self.assertEqual(0, r.pair_a[0])
        self.assertEqual(0, r.pair_b[0])

    def test_match2(self):
        ed = EditDistance(np.int32, -1)
        r = ed.distance('ab', 'ab')
        self.assertEqual(2, r.score)
        self.assertEqual(0, r.pair_a[0])
        self.assertEqual(0, r.pair_b[0])

    def test_mismatches(self):
        ed = EditDistance(np.int32, -1)
        r = ed.distance('a', 'b')
        self.assertEqual(-1, r.score)

    def test_gap(self):
        ed = EditDistance(np.int32, -1)
        r = ed.distance('ab', 'a b')
        self.assertEqual(1, r.score)

    def test_big_string(self):
        ed = EditDistance(np.int32, -1)
        n = 200
        s = 'a' * n
        r = ed.distance(s, s)
        self.assertEqual(n, r.score)


if __name__ == '__main__':
    unittest.main()
