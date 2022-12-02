# -*- encoding: utf-8 -*-

from pathlib import Path

with open(Path(__file__).parent.joinpath("inputs", "day2.txt")) as fp:
    values = [
        (ord(row[0]) - ord("A"), ord(row[2]) - ord("X")) for row in fp.readlines()
    ]


def score_1(ux: int, vx: int) -> int:
    return 1 + vx + ((1 - ((ux - vx) % 3)) % 3) * 3


def score_2(ux: int, vx: int) -> int:
    return (ux + vx - 1) % 3 + 1 + vx * 3


# part 1 - 13526
print(f"score 1 is {sum(score_1(*v) for v in values)}")

# part 2 - 14204
print(f"score 2 is {sum(score_2(*v) for v in values)}")
