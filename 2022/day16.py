# -*- encoding: utf-8 -*-

import itertools
import re
import sys

from docplex.mp.model import Model

lines = sys.stdin.read().splitlines()

pipes: dict[str, tuple[int, list[str]]] = {}
for line in lines:
    r = re.match(
        R"Valve ([A-Z]+) has flow rate=([0-9]+); tunnels? leads? to valves? (.+)",
        line,
    ).groups()

    pipes[r[0]] = (int(r[1]), r[2].split(", "))


start_pipe = "AA"
max_time = 30

#
max_time = 26
ee = [0, 1]

m = Model()

present_at = m.binary_var_dict(
    (e, t, pipe) for e, t, pipe in itertools.product(ee, range(max_time), pipes)
)
open_at = m.binary_var_dict(
    (e, t, pipe) for e, t, pipe in itertools.product(ee, range(max_time), pipes)
)

for e in ee:
    m.add_constraint(present_at[e, 0, start_pipe] == 1)

for e, pipe in itertools.product(ee, pipes):
    m.add_constraint(open_at[e, 0, pipe] == 0)

for e, t in itertools.product(ee, range(max_time)):
    m.add_constraint(m.sum(present_at[e, t, pipe] for pipe in pipes) == 1)

for e, t, pipe in itertools.product(ee, range(1, max_time), pipes):
    m.add_constraint(
        present_at[e, t, pipe]
        <= present_at[e, t - 1, pipe]
        + m.sum(present_at[e, t - 1, pipe2] for pipe2 in pipes[pipe][1])
    )

    for pipe2 in pipes:
        if pipe2 != pipe:
            m.add_constraint(present_at[e, t, pipe] <= 1 - open_at[e, t - 1, pipe2])

for e, t, pipe in itertools.product(ee, range(1, max_time), pipes):
    m.add_constraint(open_at[e, t, pipe] <= present_at[e, t, pipe])

# keeps flowing
flowing_at = m.binary_var_dict(
    (t, pipe) for t, pipe in itertools.product(range(max_time), pipes)
)

for t, pipe in itertools.product(range(max_time), pipes):
    m.add_constraint(
        flowing_at[t, pipe]
        == m.sum(open_at[e, t2, pipe] for e, t2 in itertools.product(ee, range(0, t)))
    )


# objective
m.set_objective(
    "max",
    m.sum(
        flowing_at[t, pipe] * pipes[pipe][0]
        for t, pipe in itertools.product(range(max_time), pipes)
    ),
)

m.log_output = True
s = m.solve()

print(s.get_objective_value())


# for t in range(max_time):
#     present = {
#         e: [pipe for pipe in pipes if s.get_value(present_at[e, t, pipe]) > 1e-6]
#         for e in ee
#     }
#     opent = {
#         e: [pipe for pipe in pipes if s.get_value(open_at[e, t, pipe]) > 1e-6]
#         for e in ee
#     }
#     flowing = [
#         pipe
#         for pipe in pipes
#         if any(s.get_value(flowing_at[e, t, pipe]) > 1e-6 for e in ee)
#     ]

#     p = [present[e][0] for e in ee]
#     o = [opent[e][0] if opent[e] else "-" for e in ee]

#     print(f"t={t}, at={p}, open={o}, flowing={flowing}")
