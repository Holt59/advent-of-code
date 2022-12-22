# -*- encoding: utf-8 -*-

import re
import sys

import numpy as np

VOID = 0
EMPTY = 1
WALL = 2
TILE_FROM_CHAR = {" ": VOID, ".": EMPTY, "#": WALL}


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

invert = False

y0 = 0
x0 = np.where(board[0] == EMPTY)[0][0]
r0 = "E"

if invert:
    board = board[::-1, ::-1]
    y0 = board.shape[0] - 1
    x0 = np.where(board[-1, :] == EMPTY)[0][-1]
    r0 = "W"
    # print(
    #     "\n".join(
    #         "".join(next(k for k, v in TILE_FROM_CHAR.items() if v == c) for c in row)
    #         for row in board
    #     )
    # )

# find on each row and column the first and last non-void
row_first_non_void = np.argmax(board != VOID, axis=1)
row_last_non_void = board.shape[1] - np.argmax(board[:, ::-1] != VOID, axis=1) - 1
col_first_non_void = np.argmax(board != VOID, axis=0)
col_last_non_void = board.shape[0] - np.argmax(board[::-1, :] != VOID, axis=0) - 1

print(y0, x0, r0)

for direction in directions:
    # print(f"{y0} {x0} {r0} ({direction})")
    # r1 = {"N": "S", "S": "N", "W": "E", "E": "W"}[r0]
    # print(f"{board.shape[0] - y0 - 1} {board.shape[1] - x0 - 1} {r1} ({direction})")

    if isinstance(direction, int):
        while direction > 0:
            if r0 == "E":
                xi = np.where(board[y0, x0 + 1 : x0 + direction + 1] == WALL)[0]
                # if y0 == 12 and x0 == 81:
                #     print(
                #         xi,
                #         board[y0, x0 + 1 : x0 + direction],
                #         board[y0, x0 + direction],
                #     )
                if len(xi):
                    # print("E1")
                    x0 = x0 + xi[0]
                    direction = 0
                elif (
                    x0 + direction < board.shape[1]
                    and board[y0, x0 + direction] == EMPTY
                ):
                    # print("E2")
                    x0 = x0 + direction
                    direction = 0
                elif board[y0, row_first_non_void[y0]] == WALL:
                    # print("E3")
                    x0 = row_last_non_void[y0]
                    direction = 0
                else:
                    # print("E4")
                    direction = direction - (row_last_non_void[y0] - x0) - 1
                    x0 = row_first_non_void[y0]
            elif r0 == "S":
                yi = np.where(board[y0 + 1 : y0 + direction + 1, x0] == WALL)[0]
                if len(yi):
                    # print("S1")
                    y0 = y0 + yi[0]
                    direction = 0
                elif (
                    y0 + direction < board.shape[0]
                    and board[y0 + direction, x0] == EMPTY
                ):
                    # print("S2")
                    y0 = y0 + direction
                    direction = 0
                elif board[col_first_non_void[x0], x0] == WALL:
                    print("S3")
                    y0 = col_last_non_void[x0]
                    direction = 0
                else:
                    # print("S4")
                    direction = direction - (col_last_non_void[x0] - y0) - 1
                    y0 = col_first_non_void[x0]
            elif r0 == "W":
                left = max(x0 - direction - 1, 0)
                xi = np.where(board[y0, left:x0] == WALL)[0]
                if len(xi):
                    x0 = left + xi[-1] + 1
                    direction = 0
                elif x0 - direction >= 0 and board[y0, x0 - direction] == EMPTY:
                    x0 = x0 - direction
                    direction = 0
                elif board[y0, row_last_non_void[y0]] == WALL:
                    x0 = row_first_non_void[y0]
                    direction = 0
                else:
                    # print("W", x0, row_first_non_void[y0], direction)
                    direction = direction - (x0 - row_first_non_void[y0]) - 1
                    x0 = row_last_non_void[y0]
            elif r0 == "N":
                top = max(y0 - direction - 1, 0)
                yi = np.where(board[top:y0, x0] == WALL)[0]
                if len(yi):
                    y0 = top + yi[-1] + 1
                    direction = 0
                elif y0 - direction >= 0 and board[y0 - direction, x0] == EMPTY:
                    y0 = y0 - direction
                    direction = 0
                elif board[col_last_non_void[x0], x0] == WALL:
                    y0 = col_first_non_void[x0]
                    direction = 0
                else:
                    direction = direction - (y0 - col_first_non_void[x0]) - 1
                    y0 = col_last_non_void[x0]
    else:
        r0 = {
            "E": {"L": "N", "R": "S"},
            "N": {"L": "W", "R": "E"},
            "W": {"L": "S", "R": "N"},
            "S": {"L": "E", "R": "W"},
        }[r0][direction]

if invert:
    print(y0, x0, r0, "->", end=" ")
    x0, y0, r0 = (
        board.shape[1] - x0 - 1,
        board.shape[0] - y0 - 1,
        {"N": "S", "S": "N", "W": "E", "E": "W"}[r0],
    )
print(y0, x0, r0)

score = {"E": 0, "S": 1, "W": 2, "N": 3}
answer_1 = 1000 * (1 + y0) + 4 * (1 + x0) + score[r0]
print(f"answer 1 is {answer_1}")
