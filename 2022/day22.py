# -*- encoding: utf-8 -*-

import re
import sys

import numpy as np

EMPTY = 0
VOID = 1
WALL = 2
TILE_FROM_CHAR = {" ": VOID, ".": EMPTY, "#": WALL}


board_map_s, direction_s = sys.stdin.read().split("\n\n")

# board
board_lines = board_map_s.splitlines()
max_line = max(len(line) for line in board_lines)
board_map = np.array(
    [
        [TILE_FROM_CHAR[c] for c in row] + [VOID] * (max_line - len(row))
        for row in board_map_s.splitlines()
    ]
)

directions = [
    int(p1) if p2 else p1 for p1, p2 in re.findall(R"(([0-9])+|L|R)", direction_s)
]

y0 = 0
x0 = np.where(board_map[0] == EMPTY)[0][0]
r0 = "R"
print(y0, x0)

for direction in directions:
    if isinstance(direction, int):
        if r0 == "R":
            x0 = np.argmax(board_map[y0, x0 + 1 :])
