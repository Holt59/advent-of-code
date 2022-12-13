# -*- encoding: utf-8 -*-

import sys

import numpy as np


def move(head: tuple[int, int], command: str) -> tuple[int, int]:

    h_col, h_row = head

    if command == "L":
        head = (h_col - 1, h_row)
    elif command == "R":
        head = (h_col + 1, h_row)
    elif command == "U":
        head = (h_col, h_row + 1)
    elif command == "D":
        head = (h_col, h_row - 1)

    return head


def follow(head: tuple[int, int], tail: tuple[int, int]) -> tuple[int, int]:

    h_col, h_row = head
    t_col, t_row = tail

    if abs(t_col - h_col) <= 1 and abs(t_row - h_row) <= 1:
        return tail

    return t_col + np.sign(h_col - t_col), t_row + np.sign(h_row - t_row)


def run(commands: list[str], n_blocks: int) -> list[tuple[int, int]]:

    blocks = [(0, 0) for _ in range(n_blocks)]
    visited = [blocks[-1]]

    for command in commands:
        blocks[0] = move(blocks[0], command)

        for i in range(0, n_blocks - 1):
            blocks[i + 1] = follow(blocks[i], blocks[i + 1])

        visited.append(blocks[-1])

    return visited


lines = sys.stdin.read().splitlines()

# flatten the commands
commands: list[str] = []
for line in lines:
    d, c = line.split()
    commands.extend(d * int(c))


visited_1 = run(commands, n_blocks=2)
print(f"answer 1 is {len(set(visited_1))}")

visited_2 = run(commands, n_blocks=10)
print(f"answer 2 is {len(set(visited_2))}")
