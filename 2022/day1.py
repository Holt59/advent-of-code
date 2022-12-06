# -*- encoding: utf-8 -*-

import sys

lines = sys.stdin.readlines()

# we store the list of calories for each elf in values, and we use the last element
# of values to accumulate
values: list[int] = [0]
for line in lines:
    if not line.strip():
        values = values + [0]
    else:
        values[-1] += int(line.strip())

# part 1
print(f"answer 1 is {max(values)}")

# part 2
print(f"answer 2 is {sum(sorted(values)[-3:])}")
