import math
from operator import attrgetter

range_args: attrgetter[tuple[int, int, int]] = attrgetter("start", "stop", "step")


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

    # el siguiente paso es calcular el primer numero de cada rango que sea multiplo del step
