# -*- encoding: utf-8 -*-

import sys

lines = [line.strip() for line in sys.stdin.readlines()]


def make_range(value: str) -> set[int]:
    parts = value.split("-")
    return set(range(int(parts[0]), int(parts[1]) + 1))


sections = [tuple(make_range(part) for part in line.split(",")) for line in lines]

score_1 = sum(s1.issubset(s2) or s2.issubset(s1) for s1, s2 in sections)
print(f"score 1 is {score_1}")

score_2 = sum(bool(s1.intersection(s2)) for s1, s2 in sections)
print(f"score 1 is {score_2}")
