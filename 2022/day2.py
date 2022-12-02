# -*- encoding: utf-8 -*-

from pathlib import Path

# we read the lines in a Nx2 in array with value 0/1/2 instead of A/B/C or X/Y/Z for
# easier manipulation
with open(Path(__file__).parent.joinpath("inputs", "day2.txt")) as fp:
    values = [
        (ord(row[0]) - ord("A"), ord(row[2]) - ord("X")) for row in fp.readlines()
    ]


def score_1(ux: int, vx: int) -> int:
    # explanation:
    # - (1 + vx) is just the score of the shape
    # - ((1 - (ux - vx)) % 3) gives 0 for loss, 1 for draw and 2 for win, that we
    #   can multiply with 3 to get the outcome score
    return (1 + vx) + ((1 - (ux - vx)) % 3) * 3


def score_2(ux: int, vx: int) -> int:
    # explanation:
    # - (ux + vx - 1) % 3 gives the target shape (0, 1, 2), we add one to get the score
    # - vx * 3 is simply the outcome score
    return (ux + vx - 1) % 3 + 1 + vx * 3


# part 1 - 13526
print(f"score 1 is {sum(score_1(*v) for v in values)}")

# part 2 - 14204
print(f"score 2 is {sum(score_2(*v) for v in values)}")
