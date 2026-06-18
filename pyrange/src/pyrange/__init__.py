import itertools as it
import math
import operator as op
from collections.abc import Iterator, Sequence
from dataclasses import dataclass
from numbers import Number

range_args = op.attrgetter("start", "stop", "step")


def range_intersection(*ranges: range) -> range:  # Pending for further testing
    match ranges:
        case ():
            return range(0)
        case (rng,):
            return rng

    starts, stops, steps = zip(*map(range_args, ranges))
    step = math.lcm(*steps)
    mx_step = max(steps)
    start = max(starts)
    start += abs(math.trunc(math.remainder(start, mx_step)))
    stop = min(stops)
    return range(start, stop, step)


def sum(rng: range) -> int:
    if rng:
        return (len(rng) * (rng[0] + rng[-1])) // 2
    return 0


def prod(rng: range) -> int:
    if not rng or 0 in rng:
        return 0
    elif rng.step == rng.start == 1:
        return math.factorial(rng.stop - 1)
    else:
        return math.prod(rng)


@dataclass
class Number:
    __slots__ = "x"
    x: int

    def __add__(self, rng: range):
        return range(rng.start + self.x, rng.stop + self.x, rng.step)

    __radd__ = __add__

    def __sub__(self, rng: range):
        return range(rng.start + self.x, rng.stop + self.x, rng.step)

    __rsub__ = __sub__

    def __mul__(self, rng: range):
        return range(rng.start * self.x, rng.stop * self.x, rng.step * self.x)

    __rmul__ = __mul__

    def __floordiv__(self, rng: range):
        return range(rng.start // self.x, rng.stop // self.x, rng.step // self.x)

    __rfloordiv__ = __floordiv__

    def __lshift__(self, rng: range):
        return range(rng.start << self.x, rng.stop << self.x, rng.step << self.x)

    __rlshift__ = __lshift__


def invert(rng: range) -> range:
    return range(~rng.start, ~rng.stop, -rng.step)


def pos(rng: range) -> range:
    return rng


def neg(rng: range) -> range:
    return range(-rng.start, -rng.stop, -rng.step)


inv = invert
