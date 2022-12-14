# -*- encoding: utf-8 -*-

import sys
from collections import defaultdict
from enum import Enum, auto
from typing import Callable, cast


class Cell(Enum):
    AIR = auto()
    ROCK = auto()
    SAND = auto()

    def __str__(self) -> str:
        return {Cell.AIR: ".", Cell.ROCK: "#", Cell.SAND: "O"}[self]


def print_blocks(blocks: dict[tuple[int, int], Cell]):
    """
    Print the given set of blocks on a grid.

    Args:
        blocks: Set of blocks to print.
    """
    x_min, y_min, x_max, y_max = (
        min(x for x, y in blocks),
        0,
        max(x for x, y in blocks),
        max(y for x, y in blocks),
    )

    for y in range(y_min, y_max + 1):
        print(
            "".join(str(blocks.get((x, y), Cell.AIR)) for x in range(x_min, x_max + 1))
        )


def flow(
    blocks: dict[tuple[int, int], Cell],
    stop_fn: Callable[[int, int], bool],
    fill_fn: Callable[[int, int], Cell],
) -> dict[tuple[int, int], Cell]:
    """
    Flow sands onto the given set of blocks

    Args:
        blocks: Blocks containing ROCK position. Modified in-place.
        stop_fn: Function called with the last (assumed) position of a grain of
            sand BEFORE adding it to blocks. If the function returns True, the grain
            is added and a new one is flowed, otherwise, the whole procedure stops
            and the function returns (without adding the final grain).
        fill_fn: Function called when the target position of a grain (during the
            flowing process) is missing from blocks.

    Returns:
        The input blocks.
    """

    y_max = max(y for x, y in blocks)

    while True:
        x, y = 500, 0

        while y <= y_max:

            moved = False
            for cx, cy in ((x, y + 1), (x - 1, y + 1), (x + 1, y + 1)):
                if (cx, cy) not in blocks and fill_fn(cx, cy) == Cell.AIR:
                    x, y = cx, cy
                    moved = True
                elif blocks[cx, cy] == Cell.AIR:
                    x, y = cx, cy
                    moved = True

                if moved:
                    break

            if not moved:
                break

        if stop_fn(x, y):
            break

        blocks[x, y] = Cell.SAND

    return blocks


# === inputs ===

lines = sys.stdin.read().splitlines()

paths: list[list[tuple[int, int]]] = []
for line in lines:
    parts = line.split(" -> ")
    paths.append(
        [
            cast(tuple[int, int], tuple(int(c.strip()) for c in part.split(",")))
            for part in parts
        ]
    )


blocks: dict[tuple[int, int], Cell] = {}
for path in paths:
    for start, end in zip(path[:-1], path[1:]):
        x_start = min(start[0], end[0])
        x_end = max(start[0], end[0]) + 1
        y_start = min(start[1], end[1])
        y_end = max(start[1], end[1]) + 1

        for x in range(x_start, x_end):
            for y in range(y_start, y_end):
                blocks[x, y] = Cell.ROCK

print_blocks(blocks)
print()

x_min, y_min, x_max, y_max = (
    min(x for x, y in blocks),
    0,
    max(x for x, y in blocks),
    max(y for x, y in blocks),
)

# === part 1 ===

blocks_1 = flow(
    blocks.copy(), stop_fn=lambda x, y: y > y_max, fill_fn=lambda x, y: Cell.AIR
)
print_blocks(blocks_1)
print(f"answer 1 is {sum(v == Cell.SAND for v in blocks_1.values())}")
print()

# === part 2 ===

blocks_2 = flow(
    blocks.copy(),
    stop_fn=lambda x, y: x == 500 and y == 0,
    fill_fn=lambda x, y: Cell.AIR if y < y_max + 2 else Cell.ROCK,
)
blocks_2[500, 0] = Cell.SAND
print_blocks(blocks_2)
print(f"answer 2 is {sum(v == Cell.SAND for v in blocks_2.values())}")
