# -*- encoding: utf-8 -*-

import re
import sys
from typing import Callable

import numpy as np

VOID, EMPTY, WALL = 0, 1, 2
TILE_FROM_CHAR = {" ": VOID, ".": EMPTY, "#": WALL}

SCORES = {"E": 0, "S": 1, "W": 2, "N": 3}


board_map_s, direction_s = sys.stdin.read().split("\n\n")

# board
board_lines = board_map_s.splitlines()
max_line = max(len(line) for line in board_lines)
board = np.array(
    [
        [TILE_FROM_CHAR[c] for c in row] + [VOID] * (max_line - len(row))
        for row in board_map_s.splitlines()
    ]
)

directions = [
    int(p1) if p2 else p1 for p1, p2 in re.findall(R"(([0-9])+|L|R)", direction_s)
]


# find on each row and column the first and last non-void
row_first_non_void = np.argmax(board != VOID, axis=1)
row_last_non_void = board.shape[1] - np.argmax(board[:, ::-1] != VOID, axis=1) - 1
col_first_non_void = np.argmax(board != VOID, axis=0)
col_last_non_void = board.shape[0] - np.argmax(board[::-1, :] != VOID, axis=0) - 1


faces = np.zeros_like(board)
size = np.gcd(board.shape[0], board.shape[1])
for row in range(0, board.shape[0], size):
    for col in range(row_first_non_void[row], row_last_non_void[row], size):
        faces[row : row + size, col : col + size] = faces.max() + 1

SIZE = np.gcd(*board.shape)

# TODO: deduce this from the actual cube...
faces_wrap: dict[int, dict[str, Callable[[int, int], tuple[int, int, str]]]]
if board.shape == (12, 16):  # example
    faces_wrap = {
        1: {
            "W": lambda y, x: (4, 4 + y, "S"),  # 3N
            "N": lambda y, x: (4, 11 - x, "S"),  # 2N
            "E": lambda y, x: (11 - y, 15, "W"),  # 6E
        },
        2: {
            "W": lambda y, x: (11, 19 - y, "N"),  # 6S
            "N": lambda y, x: (0, 11 - y, "S"),  # 1N
            "S": lambda y, x: (11, 11 - x, "N"),  # 5S
        },
        3: {
            "N": lambda y, x: (x - 4, 8, "E"),  # 1W
            "S": lambda y, x: (15 - x, 8, "E"),  # 5W
        },
        4: {"E": lambda y, x: (8, 19 - y, "S")},  # 6N
        5: {
            "W": lambda y, x: (7, 15 - y, "N"),  # 3S
            "S": lambda y, x: (7, 11 - x, "N"),  # 2S
        },
        6: {
            "N": lambda y, x: (19 - x, 11, "W"),  # 4E
            "E": lambda y, x: (11 - y, 11, "W"),  # 1E
            "S": lambda y, x: (19 - x, 0, "E"),  # 2W
        },
    }

else:
    faces_wrap = {
        1: {
            "W": lambda y, x: (3 * SIZE - y - 1, 0, "E"),  # 4W
            "N": lambda y, x: (2 * SIZE + x, 0, "E"),  # 6W
        },
        2: {
            "N": lambda y, x: (4 * SIZE - 1, x - 2 * SIZE, "N"),  # 6S
            "E": lambda y, x: (3 * SIZE - y - 1, 2 * SIZE - 1, "W"),  # 5E
            "S": lambda y, x: (x - SIZE, 2 * SIZE - 1, "W"),  # 3E
        },
        3: {
            "W": lambda y, x: (2 * SIZE, y - SIZE, "S"),  # 4N
            "E": lambda y, x: (SIZE - 1, SIZE + y, "N"),  # 2S
        },
        4: {
            "W": lambda y, x: (3 * SIZE - y - 1, SIZE, "E"),  # 1W
            "N": lambda y, x: (SIZE + x, SIZE, "E"),  # 3W
        },
        5: {
            "E": lambda y, x: (3 * SIZE - y - 1, 3 * SIZE - 1, "W"),  # 2E
            "S": lambda y, x: (2 * SIZE + x, SIZE - 1, "W"),  # 6E
        },
        6: {
            "W": lambda y, x: (0, y - 2 * SIZE, "S"),  # 1N
            "E": lambda y, x: (3 * SIZE - 1, y - 2 * SIZE, "N"),  # 5S
            "S": lambda y, x: (0, x + 2 * SIZE, "S"),  # 2N
        },
    }


def wrap_part_1(y0: int, x0: int, r0: str) -> tuple[int, int, str]:
    if r0 == "E":
        return y0, row_first_non_void[y0], r0
    elif r0 == "S":
        return col_first_non_void[x0], x0, r0
    elif r0 == "W":
        return y0, row_last_non_void[y0], r0
    elif r0 == "N":
        return col_last_non_void[x0], x0, r0

    assert False


def wrap_part_2(y0: int, x0: int, r0: str) -> tuple[int, int, str]:
    cube = faces[y0, x0]
    assert r0 in faces_wrap[cube]
    return faces_wrap[cube][r0](y0, x0)


def run(wrap: Callable[[int, int, str], tuple[int, int, str]]) -> tuple[int, int, str]:

    y0 = 0
    x0 = np.where(board[0] == EMPTY)[0][0]
    r0 = "E"

    for direction in directions:
        if isinstance(direction, int):
            while direction > 0:
                if r0 == "E":
                    xi = np.where(board[y0, x0 + 1 : x0 + direction + 1] == WALL)[0]
                    if len(xi):
                        x0 = x0 + xi[0]
                        direction = 0
                    elif (
                        x0 + direction < board.shape[1]
                        and board[y0, x0 + direction] == EMPTY
                    ):
                        x0 = x0 + direction
                        direction = 0
                    else:
                        y0_t, x0_t, r0_t = wrap(y0, x0, r0)
                        if board[y0_t, x0_t] == WALL:
                            x0 = row_last_non_void[y0]
                            direction = 0
                        else:
                            direction = direction - (row_last_non_void[y0] - x0) - 1
                            y0, x0, r0 = y0_t, x0_t, r0_t
                elif r0 == "S":
                    yi = np.where(board[y0 + 1 : y0 + direction + 1, x0] == WALL)[0]
                    if len(yi):
                        y0 = y0 + yi[0]
                        direction = 0
                    elif (
                        y0 + direction < board.shape[0]
                        and board[y0 + direction, x0] == EMPTY
                    ):
                        y0 = y0 + direction
                        direction = 0
                    else:
                        y0_t, x0_t, r0_t = wrap(y0, x0, r0)
                        if board[y0_t, x0_t] == WALL:
                            y0 = col_last_non_void[x0]
                            direction = 0
                        else:
                            direction = direction - (col_last_non_void[x0] - y0) - 1
                            y0, x0, r0 = y0_t, x0_t, r0_t
                elif r0 == "W":
                    left = max(x0 - direction - 1, 0)
                    xi = np.where(board[y0, left:x0] == WALL)[0]
                    if len(xi):
                        x0 = left + xi[-1] + 1
                        direction = 0
                    elif x0 - direction >= 0 and board[y0, x0 - direction] == EMPTY:
                        x0 = x0 - direction
                        direction = 0
                    else:
                        y0_t, x0_t, r0_t = wrap(y0, x0, r0)
                        if board[y0_t, x0_t] == WALL:
                            x0 = row_first_non_void[y0]
                            direction = 0
                        else:
                            direction = direction - (x0 - row_first_non_void[y0]) - 1
                            y0, x0, r0 = y0_t, x0_t, r0_t
                elif r0 == "N":
                    top = max(y0 - direction - 1, 0)
                    yi = np.where(board[top:y0, x0] == WALL)[0]
                    if len(yi):
                        y0 = top + yi[-1] + 1
                        direction = 0
                    elif y0 - direction >= 0 and board[y0 - direction, x0] == EMPTY:
                        y0 = y0 - direction
                        direction = 0
                    else:
                        y0_t, x0_t, r0_t = wrap(y0, x0, r0)
                        if board[y0_t, x0_t] == WALL:
                            y0 = col_first_non_void[x0]
                            direction = 0
                        else:
                            direction = direction - (y0 - col_first_non_void[x0]) - 1
                            y0, x0, r0 = y0_t, x0_t, r0_t
        else:
            r0 = {
                "E": {"L": "N", "R": "S"},
                "N": {"L": "W", "R": "E"},
                "W": {"L": "S", "R": "N"},
                "S": {"L": "E", "R": "W"},
            }[r0][direction]

    return y0, x0, r0


y1, x1, r1 = run(wrap_part_1)
answer_1 = 1000 * (1 + y1) + 4 * (1 + x1) + SCORES[r1]
print(f"answer 1 is {answer_1}")

y2, x2, r2 = run(wrap_part_2)
answer_2 = 1000 * (1 + y2) + 4 * (1 + x2) + SCORES[r2]
print(f"answer 2 is {answer_2}")
