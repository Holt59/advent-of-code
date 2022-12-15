# -*- encoding: utf-8 -*-

import sys

import numpy as np
import parse
from docplex.mp.model import Model

lines = sys.stdin.read().splitlines()

sensor_to_beacon: dict[tuple[int, int], tuple[int, int]] = {}

for line in lines:
    r = parse.parse(
        "Sensor at x={sx}, y={sy}: closest beacon is at x={bx}, y={by}", line
    )
    sensor_to_beacon[int(r["sx"]), int(r["sy"])] = (int(r["bx"]), int(r["by"]))

xy_max = 4_000_000 if max(sensor_to_beacon) > (1_000, 0) else 20
row = 2_000_000 if max(sensor_to_beacon) > (1_000, 0) else 10

no_beacons_row_l: list[np.ndarray] = []

for (sx, sy), (bx, by) in sensor_to_beacon.items():
    d = abs(sx - bx) + abs(sy - by)  # closest

    no_beacons_row_l.append(sx - np.arange(0, d - abs(sy - row) + 1))
    no_beacons_row_l.append(sx + np.arange(0, d - abs(sy - row) + 1))

beacons_at_row = set(bx for (bx, by) in sensor_to_beacon.values() if by == row)
no_beacons_row = set(np.concatenate(no_beacons_row_l)).difference(beacons_at_row)

print(f"answer 1 is {len(no_beacons_row)}")

# === part 2 ===

m = Model()

x, y = m.continuous_var_list(2, ub=xy_max, name=["x", "y"])

for (sx, sy), (bx, by) in sensor_to_beacon.items():
    d = abs(sx - bx) + abs(sy - by)
    m.add_constraint(m.abs(x - sx) + m.abs(y - sy) >= d + 1, ctname=f"ct_{sx}_{sy}")

m.set_objective("min", x + y)

s = m.solve()

# 10621647166538
answer_2 = 4_000_000 * int(s.get_value(x)) + int(s.get_value(y))
print(f"answer 2 is {answer_2}")
