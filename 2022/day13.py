# -*- encoding: utf-8 -*-

import json
import sys
from functools import cmp_to_key

blocks = sys.stdin.read().strip().split("\n\n")

pairs = [tuple(json.loads(p) for p in block.split("\n")) for block in blocks]


def compare(lhs: list[int | list], rhs: list[int | list]) -> int:

    for lhs_a, rhs_a in zip(lhs, rhs):
        if isinstance(lhs_a, int) and isinstance(rhs_a, int):
            if lhs_a != rhs_a:
                return rhs_a - lhs_a
        else:
            if not isinstance(lhs_a, list):
                lhs_a = [lhs_a]
            elif not isinstance(rhs_a, list):
                rhs_a = [rhs_a]
            assert isinstance(rhs_a, list) and isinstance(lhs_a, list)
            r = compare(lhs_a, rhs_a)
            if r != 0:
                return r

    return len(rhs) - len(lhs)


answer_1 = sum(i + 1 for i, (lhs, rhs) in enumerate(pairs) if compare(lhs, rhs) > 0)
print(f"answer_1 is {answer_1}")

dividers = [[[2]], [[6]]]

packets = [packet for packets in pairs for packet in packets]
packets.extend(dividers)
packets = list(reversed(sorted(packets, key=cmp_to_key(compare))))

d_index = [packets.index(d) + 1 for d in dividers]
print(f"answer 2 is {d_index[0] * d_index[1]}")
