# -*- encoding: utf-8 -*-

import sys

blocks = sys.stdin.read().split("\n\n")
values = sorted(sum(map(int, block.split())) for block in blocks)

print(f"answer 1 is {values[-1]}")
print(f"answer 2 is {sum(values[-3:])}")
