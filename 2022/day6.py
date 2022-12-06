# -*- encoding: utf-8 -*-

import sys

data = sys.stdin.read().strip()


def index_of_first_n_differents(data: str, n: int) -> int:
    for i in range(len(data)):
        if len(set(data[i : i + n])) == n:
            return i + n
    return -1


print(f"answer 1 is {index_of_first_n_differents(data, 4)}")
print(f"answer 2 is {index_of_first_n_differents(data, 14)}")
