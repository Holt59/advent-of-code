# -*- encoding: utf-8 -*-

import heapq
import sys
from typing import Callable, Iterator, TypeVar

Node = TypeVar("Node")


def dijkstra(
    start: Node,
    end: Node,
    neighbors: Callable[[Node], Iterator[Node]],
    cost: Callable[[Node, Node], float],
    heuristic: Callable[[Node, Node], float] | None = None,
) -> list[Node] | None:

    queue: list[tuple[tuple[float, float, float], Node]] = []

    visited: set[Node] = set()
    lengths: dict[Node, float] = {start: 0}
    parents: dict[Node, Node] = {}

    if heuristic is None:

        def priority(node: Node):
            c = lengths[node]
            return (c, c, c)

    else:

        def priority(node: Node):
            assert heuristic is not None
            h = heuristic(node, end)
            c = lengths[node]
            return (h + c, h, c)

    heapq.heappush(queue, (priority(start), start))

    while queue and (end not in visited):
        (_, _, length), current = heapq.heappop(queue)

        if current in visited:
            continue

        visited.add(current)

        for neighbor in neighbors(current):

            if neighbor in visited:
                continue

            neighbor_cost = length + cost(current, neighbor)

            if neighbor_cost < lengths.get(neighbor, float("inf")):
                lengths[neighbor] = length + 1
                parents[neighbor] = current

                heapq.heappush(queue, (priority(neighbor), neighbor))

    if end not in visited:
        return None

    path: list[Node] = [end]

    while path[-1] is not start:
        path.append(parents[path[-1]])

    return list(reversed(path))


def print_path(path: list[tuple[int, int]], n_rows: int, n_cols: int) -> None:
    end = path[-1]

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

n_rows = len(grid)
n_cols = len(grid[0])


def heuristic(lhs: tuple[int, int], rhs: tuple[int, int]) -> float:
    return abs(lhs[0] - rhs[0]) + abs(lhs[1] - rhs[1])


def neighbors(node: tuple[int, int]) -> Iterator[tuple[int, int]]:
    c_row, c_col = node
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


path = dijkstra(
    start=start,
    end=end,
    neighbors=neighbors,
    cost=lambda lhs, rhs: 1,
    heuristic=heuristic,
)
assert path is not None

print_path(path, n_rows=len(grid), n_cols=len(grid[0]))

answer_1 = len(path) - 1
print(f"answer 1 is {answer_1}")

answer_2 = min(
    len(path) - 1
    for start in start_s
    if (
        path := dijkstra(
            start=start,
            end=end,
            neighbors=neighbors,
            cost=lambda lhs, rhs: 1,
            heuristic=heuristic,
        )
    )
    is not None
)
print(f"answer 2 is {answer_2}")
