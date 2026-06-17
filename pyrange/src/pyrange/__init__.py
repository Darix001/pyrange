import itertools as it
import math
import operator as op
from collections.abc import Sequence
from dataclasses import dataclass

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


@dataclass(slots=True, frozen=True)
class GeometricProgression(Sequence):
    a1: int
    r: int
    n: int

    def __getitem__(self, index: int, /):
        if index < 0:
            index += self.n
        if 0 <= index < self.n:
            return self.a1 * self.r**index
        else:
            raise IndexError("GeometricProgression Index out of range.")

    def __len__(self, /):
        return self.n

    def __iter__(self, /):
        return it.accumulate(it.repeat(self.r, self.n - 1), op.mul, initial=self.a1)

    def __reversed__(self, /):
        n = self.n - 1
        last = self.a1 * (self.r**n)
        return it.accumulate(it.repeat(self.r, n), op.floordiv, initial=last)

    def index(self, number: int, /):
        index = math.log(number / self.a1, self.r)
        if index.is_integer():
            return math.trunc(index)
        else:
            raise ValueError("Number not in GeometricProgression")


if __name__ == "__main__":
    p = GeometricProgression(2, 2, 10)
    l = [2, 4, 8, 16, 32, 64, 128, 256, 512, 1024]
    assert l == list(p)
    assert l[::-1] == list(reversed(p))
    assert l[-3] == p[-3]
    assert l[5] == p[5]
    assert l.index(128) == p.index(128)
