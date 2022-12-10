# -*- encoding: utf-8 -*-

import sys

lines = sys.stdin.read().splitlines()

cycle = 1
x = 1

values = {cycle: x}

for line in lines:
    cycle += 1

    if line == "noop":
        pass
    else:
        r = int(line.split()[1])

        values[cycle] = x

        cycle += 1
        x += r

    values[cycle] = x

answer_1 = sum(c * values[c] for c in range(20, max(values.keys()) + 1, 40))
print(f"answer 1 is {answer_1}")


for i in range(6):
    for j in range(40):
        v = values[1 + i * 40 + j]

        if j >= v - 1 and j <= v + 1:
            print("#", end="")
        else:
            print(".", end="")

    print()
