# -*- encoding: utf-8 -*-

import sys

lines = sys.stdin.read().splitlines()

coeffs = {"2": 2, "1": 1, "0": 0, "-": -1, "=": -2}


def snafu2number(number: str) -> int:
    value = 0
    for c in number:
        value *= 5
        value += coeffs[c]
    return value


def number2snafu(number: int) -> str:
    values = ["0", "1", "2", "=", "-"]
    res = ""
    while number > 0:
        mod = number % 5
        res = res + values[mod]
        number = number // 5 + int(mod >= 3)
    return "".join(reversed(res))


answer_1 = number2snafu(sum(map(snafu2number, lines)))
print(f"answer 1 is {answer_1}")
