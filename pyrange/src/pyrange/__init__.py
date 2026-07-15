import math
import operator as op
from dataclasses import dataclass

range_args = op.attrgetter("start", "stop", "step")


def bytes_of_int(x: int, /):
    """Returns number of bytes necessary to represent x"""
    return math.ceil(x.bit_length() / 8)


def tobytes(rng: range, /) -> bytes:
    return b"".join(map(op.methodcaller("to_bytes", bytes_of_int(rng.stop)), rng))


def pstdev(rng: range, /) -> float:
    """Compute the popular standard deviation of the range."""
    return math.sqrt(pvar(rng))


def pvar(rng: range, /) -> float:
    """Computes the popular variance of the range."""
    if (n := len(rng)) <= 1:
        return 0.0
    return (((n**2) - 1) * (rng.step**2)) / 12


pvariance = pvar


def nbytes(rng: range, /):
    return bytes_of_int(rng.stop) * len(rng)


def var(rng: range, /) -> float:
    if (n := len(rng)) <= 1:
        return 0.0
    return ((rng.step**2) * (n * (n + 1))) / 12


def stdev(rng: range, /) -> float:
    return math.sqrt(var(rng))


def mean(rng: range, /) -> float:
    return (rng.start + rng[-1]) / 2


def min_max(rng: range, /) -> tuple[int, int]:
    t = rng.start, rng.stop
    return t if rng.step > 0 else t[::-1]


def min(rng: range, /) -> int:
    return rng.start if rng.step > 0 else rng.stop


def max(rng: range, /) -> int:
    return rng.start if rng.step < 0 else rng.stop


def isdisjoint(rng: range, other: range) -> bool:
    return not intersection(rng, other)


def intersection(*ranges: range) -> range:  # Pending for further testing
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


def issubrange(rng: range, other: range) -> bool:
    return not rng.step % other.step and rng.start in other and rng[-1] in other


def issuperrange(rng: range, other: range) -> bool:
    return issubrange(other, rng)


def sum(rng: range, /) -> int:
    if rng:
        return (len(rng) * (rng[0] + rng[-1])) // 2
    return 0


def prod(rng: range, /) -> int:
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


def invert(rng: range, /) -> range:
    return range(~rng.start, ~rng.stop, -rng.step)


def pos(rng: range, /) -> range:
    return rng


def neg(rng: range, /) -> range:
    return range(-rng.start, -rng.stop, -rng.step)


inv = invert


def gt(rng: range, other):
    pass
