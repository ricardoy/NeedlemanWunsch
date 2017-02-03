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


tolerance = 10 * 60


class Pareador(NeedlemanWunsch):

    def score(self, x, y):
        if abs(x - y) < tolerance:
            return self.simple_score(x, y)
        else:
            return -1

    def simple_score(self, ts1, ts2):
        diff = float(abs(ts1 - ts2))
        return 1 - (diff / tolerance)

    def retrieve_position(self, v, i):
        return v[i]

    def size(self, v):
        return len(v)


class PareadorTest(unittest.TestCase):

    def test(self):
        pareador = Pareador(np.float32, -0.00001)
        x = [0,
             15 * 60,
             30 * 60,
             45 * 60,
             60 * 60,
             75 * 60
             ]
        y = [47 * 60 + 50,
             2 * 3600 + 60 + 39
             ]

        r = pareador.distance(x, y)
        self.assertEqual(3, r.pair_b[0])


if __name__ == '__main__':
    unittest.main()
