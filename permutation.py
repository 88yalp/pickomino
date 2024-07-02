from itertools import product
from functools import cache
from time import perf_counter
from typing import Tuple
"""
Genarate all permutations of a list of numbers
"""


@cache
def perm(n):
    """
    Generate all permutations of numbers from 1 to n.
    """
    if n == 0:
        return [[]]
    p = perm(n - 1)
    r = []
    for l in p:
        for i in range(1, 7):
            r.append([i] + l)
    return r


@cache
def perm2(n):
    for _ in range(n):
        combined.append([1, 2, 3, 4, 5, 6])
    return product(*combined)


def perm3(n):
    return product(*(n * [[1, 2, 3, 4, 5, 6]]))


@cache
def p(target, used, dices):
    if target == 0:
        return 1
    if target < 0 or dices == 0 or len(used) == 6:
        return 0
    # print(target, used, dices)
    s = 0
    permutations = perm2(dices)
    c = 0
    for throw in permutations:
        m = 0
        c += 1
        for i in range(1, 7):
            if i in used:
                continue
            selected = throw.count(i)
            if selected == 0:
                continue
            score = WORM_SCORE if i == 6 else i
            new_target = target - selected * score
            pc = p(new_target, frozenset({*used, i}), dices - selected)
            # print(i, selected, pc, new_target, throw)
            m = max(m, pc)
        s += m
    return s / c


# for j in range(1, 10):
#     print(j, p(j, frozenset(), 8))
# for j in range(1, 10):
#     print(j, p(j, frozenset(), 8))

# assert p(0, set(), 0) == 1
# assert p(0, set(), 1) == 1
# assert p(0, set(), 2) == 1
# assert p(0, set(), 4) == 1

# assert p(1, set(), 0) == 0
# assert p(2, set(), 0) == 0
# assert p(3, set(), 0) == 0
# assert p(4, set(), 0) == 0
# assert p(5, set(), 0) == 0
# assert p(6, set(), 0) == 0

# assert p(1, set(), 1) == 1 / 6
# assert p(1, {1}, 1) == 0


# print(p(1, {1}, 1))
# print(p(0, set(), 0))
# print(p(1, set(), 1))
# print(p(1, set(), 2))
# print(p(2, set(), 2))
# print(p(3, set(), 2))
