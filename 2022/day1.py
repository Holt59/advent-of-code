# -*- encoding: utf-8 -*-

from pathlib import Path

with open(Path(__file__).parent.joinpath("inputs", "day1.txt")) as fp:
    lines = fp.readlines()

values: list[int] = [0]
for line in lines:
    if not line.strip():
        values = values + [0]
    else:
        values[-1] += int(line.strip())

# part 1
print(f"max is {max(values)}")

# part 2
print(f"sum of top 3 is {sum(sorted(values)[-3:])}")
