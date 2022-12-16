# -*- encoding: utf-8 -*-

from __future__ import annotations

import heapq
import itertools
import re
import sys
from collections import defaultdict
from typing import NamedTuple

from docplex.mp.model import Model
from docplex.mp.vartype import BinaryVarType


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


def breadth_first_search(pipes: dict[str, Pipe], pipe_1: Pipe, pipe_2: Pipe) -> int:
    queue = [(0, pipe_1)]
    visited = set()

    while queue:
        distance, current = heapq.heappop(queue)

        if current in visited:
            continue

        visited.add(current)

        if current == pipe_2:
            return distance

        for tunnel in current.tunnels:
            heapq.heappush(queue, (distance + 1, pipes[tunnel]))

    return -1


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
    for pipe_2 in pipes.values():
        distances[pipe_1, pipe_2] = breadth_first_search(pipes, pipe_1, pipe_2)

# valves with flow
relevant_pipes = [pipe for pipe in pipes.values() if pipe.flow > 0]


# nodes: list[tuple[Pipe, int, int, list[Pipe]]] = [(start_pipe, 0, 0, [])]
# best_flow: int = 0

# while nodes:
#     current, time, flow, flowing = nodes.pop(0)

#     if time == max_time:
#         if flow > best_flow:
#             best_flow = flow
#         continue

#     next_nodes: list[tuple[Pipe, int, int, list[Pipe]]] = []
#     for target in relevant_pipes:

#         if target is current or target in flowing:
#             continue

#         distance = distances[current, target] + 1

#         if time + distance >= max_time:
#             continue

#         next_nodes.append(
#             (
#                 target,
#                 time + distance,
#                 flow + distance * sum(pipe.flow for pipe in flowing) + target.flow,
#                 flowing + [target],
#             )
#         )

#     # print(time, current, flow, next_nodes)

#     if not next_nodes:
#         next_nodes.append(
#             (
#                 current,
#                 max_time,
#                 flow + sum(pipe.flow for pipe in flowing) * (max_time - time - 1),
#                 flowing,
#             )
#         )

#     nodes.extend(next_nodes)

#     # if time >= 4:
#     #     break

# print(best_flow)


# nodes = [best]
# while nodes[-1].parent is not None:
#     nodes.append(nodes[-1].parent)
# nodes = list(reversed(nodes))

# for node in nodes:
#     print(node.time, node.valve, node.flow, node.flowing)

#
start_pipe = pipes["AA"]
max_time = 30
ee = [0]

# max_time = 26
# ee = [0, 1]

m = Model()

var_out: dict[Pipe, dict[Pipe, BinaryVarType]] = {
    pipe: m.binary_var_dict(relevant_pipes) for pipe in relevant_pipes + [start_pipe]
}
var_in: dict[Pipe, dict[Pipe, BinaryVarType]] = {pipe: {} for pipe in relevant_pipes}
for p1 in var_out:
    for p2 in var_out[p1]:
        var_in[p2][p1] = var_out[p1][p2]

open_at: dict[tuple[int, Pipe], BinaryVarType] = m.continuous_var_dict(
    (
        (t, pipe)
        for t, pipe in itertools.product(range(max_time), [start_pipe] + relevant_pipes)
    ),
    lb=0,
    ub=1,
)

for time, pipe in itertools.product(range(max_time), relevant_pipes):
    m.add_constraint(open_at[time, pipe] <= m.sum())


for e in ee:
    m.add_constraint(open_at[e, 0, start_pipe] == 1)

for e, pipe in itertools.product(ee, relevant_pipes):
    m.add_constraint(open_at[e, 0, pipe] == 0)

for e, t, p1 in itertools.product(ee, range(max_time), relevant_pipes):
    from_time_and_pipe = [
        (p2, t - distances[p2, p1] - 1)
        for p2 in relevant_pipes + [start_pipe]
        if t - distances[p2, p1] - 1 >= 0 and p2 is not p1
    ]

    if from_time_and_pipe:
        m.add_constraint(
            open_at[e, t, p1]
            <= m.sum(open_at[e, t2, p2] for p2, t2 in from_time_and_pipe)
        )
    else:
        m.add_constraint(open_at[e, t, p1] == 0)

for pipe in relevant_pipes + [start_pipe]:
    m.add_constraint(
        m.sum(open_at[e, t, pipe] for e, t in itertools.product(ee, range(max_time)))
        <= 1
    )
for e, t in itertools.product(ee, range(max_time)):
    m.add_constraint(
        m.sum(open_at[e, t, pipe] for pipe in relevant_pipes + [start_pipe]) <= 1
    )

# keeps flowing
flowing_at = {
    (t, pipe): m.sum(
        open_at[e, t2, pipe] for e, t2 in itertools.product(ee, range(0, t))
    )
    for t, pipe in itertools.product(range(max_time), relevant_pipes)
}


# objective
m.set_objective(
    "max",
    m.sum(
        flowing_at[t, pipe] * pipe.flow
        for t, pipe in itertools.product(range(max_time), relevant_pipes)
    ),
)

m.log_output = True
s = m.solve()

print(s.get_objective_value())


for t in range(max_time):
    opent = {
        e: [
            pipe
            for pipe in relevant_pipes + [start_pipe]
            if s.get_value(open_at[e, t, pipe]) > 1e-8
        ]
        for e in ee
    }
    flowing = [
        pipe
        for pipe in relevant_pipes
        if any(s.get_value(flowing_at[t, pipe]) > 1e-8 for e in ee)
    ]

    assert all(len(opent[e]) <= 1 for e in ee)

    o = [opent[e][0] if opent[e] else "-" for e in ee]

    print(f"t={t}, open={o}, flowing={flowing}")
