# -*- encoding: utf-8 -*-

import itertools
import sys
from collections import defaultdict

Directions = list[
    tuple[
        str, tuple[int, int], tuple[tuple[int, int], tuple[int, int], tuple[int, int]]
    ]
]

# (Y, X)
DIRECTIONS: Directions = [
    ("N", (-1, 0), ((-1, -1), (-1, 0), (-1, 1))),
    ("S", (1, 0), ((1, -1), (1, 0), (1, 1))),
    ("W", (0, -1), ((-1, -1), (0, -1), (1, -1))),
    ("E", (0, 1), ((-1, 1), (0, 1), (1, 1))),
]


def min_max_yx(positions: set[tuple[int, int]]) -> tuple[int, int, int, int]:
    ys, xs = {y for y, x in positions}, {x for y, x in positions}
    return min(ys), min(xs), max(ys), max(xs)


def print_positions(positions: set[tuple[int, int]]):
    min_y, min_x, max_y, max_x = min_max_yx(positions)
    print(
        "\n".join(
            "".join(
                "#" if (y, x) in positions else "." for x in range(min_x - 1, max_x + 2)
            )
            for y in range(min_y - 1, max_y + 2)
        )
    )


def round(
    positions: set[tuple[int, int]],
    directions: Directions,
):
    to_move: dict[tuple[int, int], list[tuple[int, int]]] = defaultdict(lambda: [])
    for (y, x) in positions:
        elves = {
            (dy, dx): (y + dy, x + dx) in positions
            for dy, dx in itertools.product((-1, 0, 1), (-1, 0, 1))
            if (dy, dx) != (0, 0)
        }

        if not any(elves.values()):
            to_move[y, x].append((y, x))
            continue

        found: str | None = None
        for d, (dy, dx), d_yx_check in directions:
            if not any(elves[dy, dx] for dy, dx in d_yx_check):
                found = d
                to_move[y + dy, x + dx].append((y, x))
                break
        if found is None:
            to_move[y, x].append((y, x))

    positions.clear()
    for ty, tx in to_move:
        if len(to_move[ty, tx]) > 1:
            positions.update(to_move[ty, tx])
        else:
            positions.add((ty, tx))

    directions.append(directions.pop(0))


POSITIONS = {
    (i, j)
    for i, row in enumerate(sys.stdin.read().splitlines())
    for j, col in enumerate(row)
    if col == "#"
}

# === part 1 ===

p1, d1 = POSITIONS.copy(), DIRECTIONS.copy()
for r in range(10):
    round(p1, d1)

min_y, min_x, max_y, max_x = min_max_yx(p1)
answer_1 = sum(
    (y, x) not in p1 for y in range(min_y, max_y + 1) for x in range(min_x, max_x + 1)
)
print(f"answer 1 is {answer_1}")

# === part 2 ===

p2, d2 = POSITIONS.copy(), DIRECTIONS.copy()
answer_2 = 0
while True:
    answer_2 += 1
    backup = p2.copy()
    round(p2, d2)

    if backup == p2:
        break

print(f"answer 2 is {answer_2}")
