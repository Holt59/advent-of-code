# -*- encoding: utf-8 -*-

import sys
from collections import defaultdict

import numpy as np

lines: list[str] = sys.stdin.read().splitlines()

sections: list[tuple[tuple[int, int], tuple[int, int]]] = [
    (
        (
            int(line.split(" -> ")[0].split(",")[0]),
            int(line.split(" -> ")[0].split(",")[1]),
        ),
        (
            int(line.split(" -> ")[1].split(",")[0]),
            int(line.split(" -> ")[1].split(",")[1]),
        ),
    )
    for line in lines
]

np_sections = np.array(sections).reshape(-1, 4)

x_min, x_max, y_min, y_max = (
    min(np_sections[:, 0].min(), np_sections[:, 2].min()),
    max(np_sections[:, 0].max(), np_sections[:, 2].max()),
    min(np_sections[:, 1].min(), np_sections[:, 3].min()),
    max(np_sections[:, 1].max(), np_sections[:, 3].max()),
)

counts_1 = np.zeros((y_max + 1, x_max + 1), dtype=int)
counts_2 = counts_1.copy()

for (x1, y1), (x2, y2) in sections:

    x_rng = range(x1, x2 + 1, 1) if x2 >= x1 else range(x1, x2 - 1, -1)
    y_rng = range(y1, y2 + 1, 1) if y2 >= y1 else range(y1, y2 - 1, -1)

    if x1 == x2 or y1 == y2:
        counts_1[list(y_rng), list(x_rng)] += 1
        counts_2[list(y_rng), list(x_rng)] += 1
    elif abs(x2 - x1) == abs(y2 - y1):
        for i, j in zip(y_rng, x_rng):
            counts_2[i, j] += 1

answer_1 = (counts_1 >= 2).sum()
print(f"answer 1 is {answer_1}")

answer_2 = (counts_2 >= 2).sum()
print(f"answer 2 is {answer_2}")
