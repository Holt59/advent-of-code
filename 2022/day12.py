# -*- encoding: utf-8 -*-

import heapq
import sys
from typing import Iterator


def dijkstra(
    start: tuple[int, int], end: tuple[int, int], grid: list[list[int]]
) -> list[tuple[int, int]] | None:
    n_rows = len(grid)
    n_cols = len(grid[0])

    def heuristic(row: int, col: int) -> int:
        return abs(end[0] - row) + abs(end[1] - col)

    def neighbors(row: int, col: int) -> Iterator[tuple[int, int]]:
        for n_row, n_col in (
            (c_row - 1, c_col),
            (c_row + 1, c_col),
            (c_row, c_col - 1),
            (c_row, c_col + 1),
        ):

            if not (n_row >= 0 and n_row < n_rows and n_col >= 0 and n_col < n_cols):
                continue

            if grid[n_row][n_col] > grid[c_row][c_col] + 1:
                continue

            yield n_row, n_col

    queue: list[tuple[tuple[int, int], tuple[int, int]]] = []

    visited: set[tuple[int, int]] = set()
    lengths: dict[tuple[int, int], int] = {}
    parents: dict[tuple[int, int], tuple[int, int]] = {}

    heapq.heappush(queue, ((heuristic(start[0], start[1]), 0), start))

    while queue and (end not in visited):
        (_, length), (c_row, c_col) = heapq.heappop(queue)

        visited.add((c_row, c_col))

        for n_row, n_col in neighbors(c_row, c_col):

            if (n_row, n_col) in visited:
                continue

            if length + 1 < lengths.get((n_row, n_col), n_rows * n_cols):
                lengths[n_row, n_col] = length + 1
                parents[n_row, n_col] = (c_row, c_col)

                heapq.heappush(
                    queue,
                    (
                        (heuristic(n_row, n_col) + length + 1, length + 1),
                        (n_row, n_col),
                    ),
                )

    if end not in visited:
        return None

    path: list[tuple[int, int]] = [end]

    while path[-1] != start:
        path.append(parents[path[-1]])

    return list(reversed(path))


def print_path(path: list[tuple[int, int]], n_rows: int, n_cols: int) -> None:
    _, end = path[0], path[-1]

    graph = [["." for _c in range(n_cols)] for _r in range(n_rows)]
    graph[end[0]][end[1]] = "E"

    for i in range(0, len(path) - 1):
        cr, cc = path[i]
        nr, nc = path[i + 1]

        if cr == nr and nc == cc - 1:
            graph[cr][cc] = "<"
        elif cr == nr and nc == cc + 1:
            graph[cr][cc] = ">"
        elif cr == nr - 1 and nc == cc:
            graph[cr][cc] = "v"
        elif cr == nr + 1 and nc == cc:
            graph[cr][cc] = "^"
        else:
            assert False, "{} -> {} infeasible".format(path[i], path[i + 1])

    print("\n".join("".join(row) for row in graph))


lines = sys.stdin.read().splitlines()

grid = [[ord(cell) - ord("a") for cell in line] for line in lines]

start: tuple[int, int]
end: tuple[int, int]

# for part 2
start_s: list[tuple[int, int]] = []

for i_row, row in enumerate(grid):
    for i_col, col in enumerate(row):
        if chr(col + ord("a")) == "S":
            start = (i_row, i_col)
            start_s.append(start)
        elif chr(col + ord("a")) == "E":
            end = (i_row, i_col)
        elif col == 0:
            start_s.append((i_row, i_col))

# fix values
grid[start[0]][start[1]] = 0
grid[end[0]][end[1]] = ord("z") - ord("a")

path = dijkstra(start, end, grid)
assert path is not None

print_path(path, n_rows=len(grid), n_cols=len(grid[0]))

answer_1 = len(path) - 1
print(f"answer 1 is {answer_1}")

answer_2 = min(
    len(path) - 1
    for start in start_s
    if (path := dijkstra(start, end, grid)) is not None
)
print(f"answer 2 is {answer_2}")
