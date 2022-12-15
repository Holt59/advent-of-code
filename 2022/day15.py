# -*- encoding: utf-8 -*-

import sys

import numpy as np
import parse


def part1(sensor_to_beacon: dict[tuple[int, int], tuple[int, int]], row: int) -> int:

    no_beacons_row_l: list[np.ndarray] = []

    for (sx, sy), (bx, by) in sensor_to_beacon.items():
        d = abs(sx - bx) + abs(sy - by)  # closest

        no_beacons_row_l.append(sx - np.arange(0, d - abs(sy - row) + 1))
        no_beacons_row_l.append(sx + np.arange(0, d - abs(sy - row) + 1))

    beacons_at_row = set(bx for (bx, by) in sensor_to_beacon.values() if by == row)
    no_beacons_row = set(np.concatenate(no_beacons_row_l)).difference(beacons_at_row)

    return len(no_beacons_row)


def part2_intervals(
    sensor_to_beacon: dict[tuple[int, int], tuple[int, int]], xy_max: int
) -> tuple[int, int, int]:
    from tqdm import trange

    for y in trange(xy_max + 1):
        its: list[tuple[int, int]] = []
        for (sx, sy), (bx, by) in sensor_to_beacon.items():
            d = abs(sx - bx) + abs(sy - by)
            dx = d - abs(sy - y)

            if dx >= 0:
                its.append((max(0, sx - dx), min(sx + dx, xy_max)))

        its = sorted(its)
        s, e = its[0]

        for si, ei in its[1:]:
            if si > e + 1:
                return si - 1, y, 4_000_000 * (si - 1) + y
            if ei > e:
                e = ei

    return (0, 0, 0)


def part2_cplex(
    sensor_to_beacon: dict[tuple[int, int], tuple[int, int]], xy_max: int
) -> tuple[int, int, int]:
    from docplex.mp.model import Model

    m = Model()

    x, y = m.continuous_var_list(2, ub=xy_max, name=["x", "y"])

    for (sx, sy), (bx, by) in sensor_to_beacon.items():
        d = abs(sx - bx) + abs(sy - by)
        m.add_constraint(m.abs(x - sx) + m.abs(y - sy) >= d + 1, ctname=f"ct_{sx}_{sy}")

    m.set_objective("min", x + y)

    s = m.solve()

    vx = int(s.get_value(x))
    vy = int(s.get_value(y))
    return vx, vy, 4_000_000 * vx + vy


lines = sys.stdin.read().splitlines()

sensor_to_beacon: dict[tuple[int, int], tuple[int, int]] = {}

for line in lines:
    r = parse.parse(
        "Sensor at x={sx}, y={sy}: closest beacon is at x={bx}, y={by}", line
    )
    sensor_to_beacon[int(r["sx"]), int(r["sy"])] = (int(r["bx"]), int(r["by"]))

xy_max = 4_000_000 if max(sensor_to_beacon) > (1_000, 0) else 20
row = 2_000_000 if max(sensor_to_beacon) > (1_000, 0) else 10

print(f"answer 1 is {part1(sensor_to_beacon, row)}")

# x, y, a2 = part2_cplex(sensor_to_beacon, xy_max)
x, y, a2 = part2_intervals(sensor_to_beacon, xy_max)
print(f"answer 2 is {a2} (x={x}, y={y})")
