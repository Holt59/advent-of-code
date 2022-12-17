# -*- encoding: utf-8 -*-

"""
Part 2:
    The idea is to find a repeatable tower to not have to calculate up to the given
    number.

    The issue here is that you can consume a variable number of jets per rock, so you
    cannot simply build a tower of hight LCM(len(ROCKS), len(JETS)), you need to find
    a repeat point. The easiest repeat point is one where the incoming rock is the
    first one (horizontal line) at the same place in the jet sequence.

    The first rock cannot pass any rock present in the tower, so we know if we start
    with the same sequence of jets, it will end at the exact same positions (bottom)
    and following rocks will follow the same pattern.

    What I did:
      1. Place rocks as in part 1 but keep tracks of the (rock 0, jet) previously done
         (where jet is the index in the sequence, not just '<' or '>'). When a
         (rock 0, jet) pair gets repeats, stop the process.
      2. At this points, you have places N rocks and the number of rocks between the
         two (rock 0, jet) points is K. You have 1000... - N rocks to place, and you
         can repeat sequence of K blocks by building towers of hight K starting with
         rock 0 and at position "jet" in the sequence of jets.
      3. Once this is done, you are left with (1000... - N) % K rocks to place, starting
         again at index "jet" in the sequence of jets.
"""

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


def tower_hight(tower: np.ndarray) -> int:
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
) -> tuple[np.ndarray, int, tuple[int, int], int]:

    tower = EMPTY_BLOCKS.copy()
    tower[0, :] = init

    done_at: dict[tuple[int, int], int] = {}
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

        tower[rock_y, rock_x] = True

    return tower, rock_count, (i_rock, i_jet), done_at.get((i_rock, i_jet), -1)


line = sys.stdin.read().strip()

tower, *_ = build_tower(2022, line)
answer_1 = tower_hight(tower)
print(f"answer 1 is {answer_1}")

total_rocks = 1_000_000_000_000
tower_1, n_rocks_1, (i_rocks_1, i_jet_1), prev_1 = build_tower(total_rocks, line, True)

# shift the line
line = line[i_jet_1:] + line[:i_jet_1]

# remaining rocks
remaining_rocks = total_rocks - n_rocks_1
n_repeat_rocks = n_rocks_1 - prev_1

# repeated tower
n_repeat_towers = remaining_rocks // n_repeat_rocks
tower_repeat, *_ = build_tower(n_repeat_rocks, line)

# remaining tower
remaining_rocks = remaining_rocks % n_repeat_rocks
tower_remaining, *_ = build_tower(remaining_rocks, line)

answer_2 = (
    tower_hight(tower_1)
    + tower_hight(tower_repeat) * n_repeat_towers
    + tower_hight(tower_remaining)
)
print(f"answer 2 is {answer_2}")
