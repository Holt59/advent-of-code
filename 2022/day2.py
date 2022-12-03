# -*- encoding: utf-8 -*-

import sys

lines = sys.stdin.readlines()

# the solution relies on replacing rock / paper / scissor by values 0 / 1 / 2 and using
# modulo-3 arithmetic
#
# in modulo-3 arithmetic, the winning move is 1 + the opponent move (e.g., winning move
# if opponent plays 0 is 1, or 0 if opponent plays 2 (0 = (2 + 1 % 3)))
#

# we read the lines in a Nx2 in array with value 0/1/2 instead of A/B/C or X/Y/Z for
# easier manipulation
values = [(ord(row[0]) - ord("A"), ord(row[2]) - ord("X")) for row in lines]


def score_1(ux: int, vx: int) -> int:
    # here ux and vx are both moves: 0 = rock, 1 = paper, 2 = scissor
    #

    # 1. to get the score of the move/shape, we simply add 1 -> vx + 1
    # 2. to get the score of the outcome (loss/draw/win), we use the fact that the
    #    winning hand is always the opponent hand (ux) + 1 in modulo-3 arithmetic:
    #    - (ux - vx) % 3 gives us 0 for a draw, 1 for a loss and 2 for a win
    #    - 1 - ((ux - vx) % 3) gives us -1 for a win, 0 for a loss and 1 for a draw
    #    - (1 - ((ux - vx) % 3)) gives us 0 / 1 / 2 for loss / draw / win
    #    - the above can be rewritten as ((1 - (ux - vx)) % 3)
    #    we can then simply multiply this by 3 to get the outcome score
    #
    return (vx + 1) + ((1 - (ux - vx)) % 3) * 3


def score_2(ux: int, vx: int) -> int:
    # here ux is the opponent move (0 = rock, 1 = paper, 2 = scissor) and vx is the
    # outcome (0 = loss, 1 = draw, 2 = win)
    #

    # 1. to get the score to the move/shape, we need to find it (as 0, 1 or 2) and then
    #    add 1 to it
    #    - (vx - 1) gives the offset from the opponent shape (-1 for a loss, 0 for a
    #      draw and 1 for a win)
    #    - from the offset, we can retrieve the shape by adding the opponent shape and
    #      using modulo-3 arithmetic -> (ux + vx - 1) % 3
    #    - we then add 1 to get the final shape score
    # 2. to get the score of the outcome, we can simply multiply vx by 3 -> vx * 3
    return (ux + vx - 1) % 3 + 1 + vx * 3


# part 1 - 13526
print(f"score 1 is {sum(score_1(*v) for v in values)}")

# part 2 - 14204
print(f"score 2 is {sum(score_2(*v) for v in values)}")
