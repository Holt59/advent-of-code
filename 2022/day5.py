# -*- encoding: utf-8 -*-

import copy
import sys

blocks_s, moves_s = (part.splitlines() for part in sys.stdin.read().split("\n\n"))

blocks: dict[str, list[str]] = {stack: [] for stack in blocks_s[-1].split()}

# this codes assumes that the lines are regular, i.e., 4 characters per "crate" in the
# form of '[X] ' (including the trailing space)
#
for block in blocks_s[-2::-1]:
    for stack, index in zip(blocks, range(0, len(block), 4)):
        crate = block[index + 1 : index + 2].strip()

        if crate:
            blocks[stack].append(crate)

# part 1 - deep copy for part 2
blocks_1 = copy.deepcopy(blocks)

for move in moves_s:
    _, count_s, _, from_, _, to_ = move.strip().split()

    for _i in range(int(count_s)):
        blocks_1[to_].append(blocks_1[from_].pop())

# part 2
blocks_2 = copy.deepcopy(blocks)

for move in moves_s:
    _, count_s, _, from_, _, to_ = move.strip().split()
    count = int(count_s)

    blocks_2[to_].extend(blocks_2[from_][-count:])
    del blocks_2[from_][-count:]

answer_1 = "".join(s[-1] for s in blocks_1.values())
print(f"answer 1 is {answer_1}")

answer_2 = "".join(s[-1] for s in blocks_2.values())
print(f"answer 2 is {answer_2}")
