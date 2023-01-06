# -*- encoding: utf-8 -*-

import string
import sys

lines = [line.strip() for line in sys.stdin.readlines()]

# extract content of each part
parts = [(set(line[: len(line) // 2]), set(line[len(line) // 2 :])) for line in lines]

# priorities
priorities = {c: i + 1 for i, c in enumerate(string.ascii_letters)}

# part 1
part1 = sum(priorities[c] for p1, p2 in parts for c in p1.intersection(p2))
print(f"score 1 is {part1}")

# part 2
n_per_group = 3
part2 = sum(
    priorities[c]
    for i in range(0, len(lines), n_per_group)
    for c in set(lines[i]).intersection(*lines[i + 1 : i + n_per_group])
)
print(f"score 2 is {part2}")
