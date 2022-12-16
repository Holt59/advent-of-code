# -*- encoding: utf-8 -*-

from __future__ import annotations

import heapq
import itertools
import re
import sys
from collections import defaultdict
from typing import FrozenSet, NamedTuple

from tqdm import tqdm


class Pipe(NamedTuple):
    name: str
    flow: int
    tunnels: list[str]

    def __lt__(self, other: object) -> bool:
        return isinstance(other, Pipe) and other.name < self.name

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Pipe) and other.name == self.name

    def __hash__(self) -> int:
        return hash(self.name)

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return self.name


def breadth_first_search(pipes: dict[str, Pipe], pipe: Pipe) -> dict[Pipe, int]:
    """
    Runs a BFS from the given pipe and return the shortest distance (in term of hops)
    to all other pipes.
    """
    queue = [(0, pipe_1)]
    visited = set()
    distances: dict[Pipe, int] = {}

    while len(distances) < len(pipes):
        distance, current = heapq.heappop(queue)

        if current in visited:
            continue

        visited.add(current)
        distances[current] = distance

        for tunnel in current.tunnels:
            heapq.heappush(queue, (distance + 1, pipes[tunnel]))

    return distances


def update_with_better(
    node_at_times: dict[FrozenSet[Pipe], int], flow: int, flowing: FrozenSet[Pipe]
) -> None:
    node_at_times[flowing] = max(node_at_times[flowing], flow)


def part_1(
    start_pipe: Pipe,
    max_time: int,
    distances: dict[tuple[Pipe, Pipe], int],
    relevant_pipes: FrozenSet[Pipe],
):

    node_at_times: dict[int, dict[Pipe, dict[FrozenSet[Pipe], int]]] = defaultdict(
        lambda: defaultdict(lambda: defaultdict(lambda: 0))
    )
    node_at_times[0] = {start_pipe: {frozenset(): 0}}

    for time in range(max_time):
        for c_pipe, nodes in node_at_times[time].items():
            for flowing, flow in nodes.items():
                for target in relevant_pipes:

                    distance = distances[c_pipe, target] + 1
                    if time + distance >= max_time or target in flowing:
                        continue

                    update_with_better(
                        node_at_times[time + distance][target],
                        flow + sum(pipe.flow for pipe in flowing) * distance,
                        flowing | {target},
                    )

                update_with_better(
                    node_at_times[max_time][c_pipe],
                    flow + sum(pipe.flow for pipe in flowing) * (max_time - time),
                    flowing,
                )

    return max(
        flow
        for nodes_of_pipe in node_at_times[max_time].values()
        for flow in nodes_of_pipe.values()
    )


def part_2(
    start_pipe: Pipe,
    max_time: int,
    distances: dict[tuple[Pipe, Pipe], int],
    relevant_pipes: FrozenSet[Pipe],
):
    def compute(pipes_for_me: FrozenSet[Pipe]) -> int:
        return part_1(start_pipe, max_time, distances, pipes_for_me) + part_1(
            start_pipe, max_time, distances, relevant_pipes - pipes_for_me
        )

    combs = [
        frozenset(relevant_pipes_1)
        for r in range(2, len(relevant_pipes) // 2 + 1)
        for relevant_pipes_1 in itertools.combinations(relevant_pipes, r)
    ]

    return max(compute(comb) for comb in tqdm(combs))


# === MAIN ===


lines = sys.stdin.read().splitlines()


pipes: dict[str, Pipe] = {}
for line in lines:
    r = re.match(
        R"Valve ([A-Z]+) has flow rate=([0-9]+); tunnels? leads? to valves? (.+)",
        line,
    )
    assert r

    g = r.groups()

    pipes[g[0]] = Pipe(g[0], int(g[1]), g[2].split(", "))

# compute distances from one valve to any other
distances: dict[tuple[Pipe, Pipe], int] = {}
for pipe_1 in pipes.values():
    distances.update(
        {
            (pipe_1, pipe_2): distance
            for pipe_2, distance in breadth_first_search(pipes, pipe_1).items()
        }
    )

# valves with flow
relevant_pipes = frozenset(pipe for pipe in pipes.values() if pipe.flow > 0)


# 1651, 1653
print(part_1(pipes["AA"], 30, distances, relevant_pipes))

# 1707, 2223
print(part_2(pipes["AA"], 26, distances, relevant_pipes))
