import math
from dataclasses import dataclass
from operator import attrgetter

range_args = attrgetter("start", "stop", "step")


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


if __name__ == "__main__":
    import builtins

    rng = range(17, 890, 17)
    print(sum(rng), builtins.sum(rng))

    print(rng // Number(2))
