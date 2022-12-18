# -*- encoding: utf-8 -*-

import sys
from typing import Sequence, TypeVar

import numpy as np

T = TypeVar("T")


def print_tower(tower: np.ndarray, out: str = "#"):
    print("-" * (tower.shape[1] + 2))
    non_empty = False
    for row in reversed(range(1, tower.shape[0])):
        if not non_empty and not tower[row, :].any():
            continue
        non_empty = True
        print("|" + "".join(out if c else "." for c in tower[row, :]) + "|")
    print("+" + "-" * tower.shape[1] + "+")


def tower_height(tower: np.ndarray) -> int:
    return int(tower.shape[0] - tower[::-1, :].argmax(axis=0).min() - 1)


def next_cycle(sequence: Sequence[T], index: int) -> tuple[T, int]:
    t = sequence[index]
    index = (index + 1) % len(sequence)
    return t, index


ROCKS = [
    np.array([(0, 0), (0, 1), (0, 2), (0, 3)]),
    np.array([(0, 1), (1, 0), (1, 1), (1, 2), (2, 1)]),
    np.array([(0, 0), (0, 1), (0, 2), (1, 2), (2, 2)]),
    np.array([(0, 0), (1, 0), (2, 0), (3, 0)]),
    np.array([(0, 0), (0, 1), (1, 0), (1, 1)]),
]

WIDTH = 7
START_X = 2

EMPTY_BLOCKS = np.zeros((10, WIDTH), dtype=bool)


def build_tower(
    n_rocks: int,
    jets: str,
    early_stop: bool = False,
    init: np.ndarray = np.ones(WIDTH, dtype=bool),
) -> tuple[np.ndarray, int, int, dict[int, int]]:

    tower = EMPTY_BLOCKS.copy()
    tower[0, :] = init

    done_at: dict[tuple[int, int], int] = {}
    heights: dict[int, int] = {}
    i_jet, i_rock = 0, 0
    rock_count = 0

    for rock_count in range(n_rocks):

        if early_stop:
            if i_rock == 0 and (i_rock, i_jet) in done_at:
                break
            done_at[i_rock, i_jet] = rock_count

        y_start = tower.shape[0] - tower[::-1, :].argmax(axis=0).min() + 3
        rock, i_rock = next_cycle(ROCKS, i_rock)

        rock_y = rock[:, 0] + y_start
        rock_x = rock[:, 1] + START_X

        if rock_y.max() >= tower.shape[0]:
            tower = np.concatenate([tower, EMPTY_BLOCKS], axis=0)

        while True:

            jet, i_jet = next_cycle(jets, i_jet)

            dx = 0
            if jet == ">" and rock_x.max() < WIDTH - 1:
                dx = 1
            elif jet == "<" and rock_x.min() > 0:
                dx = -1

            if dx != 0 and not tower[rock_y, rock_x + dx].any():
                rock_x = rock_x + dx

            # move down
            rock_y -= 1

            if tower[rock_y, rock_x].any():
                rock_y += 1
                break

        heights[rock_count] = tower_height(tower)
        tower[rock_y, rock_x] = True

    return tower, rock_count, done_at.get((i_rock, i_jet), -1), heights


line = sys.stdin.read().strip()

tower, *_ = build_tower(2022, line)
answer_1 = tower_height(tower)
print(f"answer 1 is {answer_1}")

TOTAL_ROCKS = 1_000_000_000_000
tower_1, n_rocks_1, prev_1, heights_1 = build_tower(TOTAL_ROCKS, line, True)
assert prev_1 > 0

# 2767 1513
remaining_rocks = TOTAL_ROCKS - n_rocks_1
n_repeat_rocks = n_rocks_1 - prev_1
n_repeat_towers = remaining_rocks // n_repeat_rocks

base_height = heights_1[prev_1]
repeat_height = heights_1[prev_1 + n_repeat_rocks - 1] - heights_1[prev_1]
remaining_height = (
    heights_1[prev_1 + remaining_rocks % n_repeat_rocks] - heights_1[prev_1]
)

answer_2 = base_height + (n_repeat_towers + 1) * repeat_height + remaining_height
print(f"answer 2 is {answer_2}")
