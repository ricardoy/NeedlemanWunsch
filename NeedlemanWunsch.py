import numpy as np
from abc import ABCMeta
from abc import abstractmethod

UP = 1
DIAGONAL = 2
LEFT = 3


class Alignment(object):

    def __init__(self, a, b, score, pair_a, pair_b):
        self.a = a
        self.pair_a = pair_a
        self.b = b
        self.pair_b = pair_b
        self.score = score


class NeedlemanWunsch(object):

    __metaclass__ = ABCMeta

    def __init__(self, dtype, gap_score):
        self.dtype = dtype
        self.gap_score = gap_score

    @abstractmethod
    def score(self, a, b):
        return

    @abstractmethod
    def retrieve_position(self, v, i):
        return

    @abstractmethod
    def size(self, v):
        return

    def align_score(self, a, i, b, j):
        a_i = self.retrieve_position(a, i - 1)
        b_j = self.retrieve_position(b, j - 1)
        return self.score(a_i, b_j)

    def distance(self, a, b):
        n = self.size(a)
        m = self.size(b)

        D = np.zeros((n + 1, m + 1), dtype=self.dtype)
        E = np.zeros((n + 1, m + 1), dtype=np.int32)
        for i in range(0, n + 1):
            D[i, 0] = i * self.gap_score
        for j in range(0, m + 1):
            D[0, j] = j * self.gap_score

        for i in range(1, n + 1):
            for j in range(1, m + 1):
                up = D[i - 1, j] + self.gap_score
                left = D[i, j - 1] + self.gap_score
                diagonal = D[i - 1, j - 1] + self.align_score(a, i, b, j)

                best_score = max(up, left, diagonal)

                D[i, j] = best_score
                if best_score == up:
                    E[i, j] = UP
                elif best_score == left:
                    E[i, j] = LEFT
                else:
                    E[i, j] = DIAGONAL

        i = n
        j = m
        a_pair = -1 * np.ones(n, dtype=np.int32)
        b_pair = -1 * np.ones(m, dtype=np.int32)
        while i >= 0 and j >= 0:
            if E[i, j] == DIAGONAL and self.align_score(a, i, b, j) > 0:
                a_pair[i - 1] = j - 1
                b_pair[j - 1] = i - 1
                i -= 1
                j -= 1
            elif E[i, j] == LEFT:
                j -= 1
            else:
                i -= 1

        return Alignment(a, b, D[n, m], a_pair, b_pair)
