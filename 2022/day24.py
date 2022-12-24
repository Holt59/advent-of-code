# -*- encoding: utf-8 -*-

import heapq
import math
import sys
from collections import defaultdict

lines = sys.stdin.read().splitlines()

winds = {
    (i - 1, j - 1, lines[i][j])
    for i in range(1, len(lines) - 1)
    for j in range(1, len(lines[i]) - 1)
    if lines[i][j] != "."
}

n_rows, n_cols = len(lines) - 2, len(lines[0]) - 2
CYCLE = math.lcm(n_rows, n_cols)

# for each row, set of forward winds
east_winds = [{j for j in range(n_cols) if (i, j, ">") in winds} for i in range(n_rows)]
west_winds = [{j for j in range(n_cols) if (i, j, "<") in winds} for i in range(n_rows)]
north_winds = [
    {i for i in range(n_rows) if (i, j, "^") in winds} for j in range(n_cols)
]
south_winds = [
    {i for i in range(n_rows) if (i, j, "v") in winds} for j in range(n_cols)
]


def run(start: tuple[int, int], start_cycle: int, end: tuple[int, int]):
    def heuristic(y: int, x: int) -> int:
        return abs(end[0] - y) + abs(end[1] - x)

    # (distance + heuristic, distance, start_pos)
    queue = [(heuristic(start[0], start[1]), 0, ((start[0], start[1]), start_cycle))]
    visited: set[tuple[tuple[int, int], int]] = set()
    distances: dict[tuple[int, int], dict[int, int]] = defaultdict(lambda: {})

    while queue:
        _, distance, ((y, x), cycle) = heapq.heappop(queue)
        # print(y, x, distance, cycle)

        if ((y, x), cycle) in visited:
            continue

        distances[y, x][cycle] = distance

        visited.add(((y, x), cycle))

        if (y, x) == (end[0], end[1]):
            break

        for dy, dx in (0, 0), (-1, 0), (1, 0), (0, -1), (0, 1):
            ty = y + dy
            tx = x + dx

            n_cycle = (cycle + 1) % CYCLE

            if (ty, tx) == end:
                heapq.heappush(queue, (distance + 1, distance + 1, ((ty, tx), n_cycle)))
                break

            if ((ty, tx), n_cycle) in visited:
                continue

            if (ty, tx) != start and (ty < 0 or tx < 0 or ty >= n_rows or tx >= n_cols):
                continue

            if (ty, tx) != start:
                if any(ty == (vy + n_cycle) % n_rows for vy in south_winds[tx]):
                    continue
                if any(ty == (vy - n_cycle) % n_rows for vy in north_winds[tx]):
                    continue
                if any(tx == (vx - n_cycle) % n_cols for vx in west_winds[ty]):
                    continue
                if any(tx == (vx + n_cycle) % n_cols for vx in east_winds[ty]):
                    continue

            # print(f"{y} {x} [{cycle}] -> {ty} {tx}")

            heapq.heappush(
                queue,
                ((heuristic(ty, tx) + distance + 1, distance + 1, ((ty, tx), n_cycle))),
            )

    return distances, next(iter(distances[end].values()))


start = (
    -1,
    next(j for j in range(1, len(lines[0]) - 1) if lines[0][j] == ".") - 1,
)
end = (
    n_rows,
    next(j for j in range(1, len(lines[-1]) - 1) if lines[-1][j] == ".") - 1,
)

distances_1, forward_1 = run(start, 0, end)
print(f"answer 1 is {forward_1}")

distances_2, return_1 = run(end, next(iter(distances_1[end].keys())), start)
distances_3, forward_2 = run(start, next(iter(distances_2[start].keys())), end)
print(f"answer 2 is {forward_1 + return_1 + forward_2}")
