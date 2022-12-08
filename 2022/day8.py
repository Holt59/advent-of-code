# -*- encoding: utf-8 -*-

import sys

import numpy as np

lines = sys.stdin.read().splitlines()

trees = np.array([[int(x) for x in row] for row in lines])

# answer 1
highest_trees = np.ones(trees.shape + (4,), dtype=int) * -1
highest_trees[1:-1, 1:-1] = [
    [
        [
            trees[:i, j].max(),
            trees[i + 1 :, j].max(),
            trees[i, :j].max(),
            trees[i, j + 1 :].max(),
        ]
        for j in range(1, trees.shape[1] - 1)
    ]
    for i in range(1, trees.shape[0] - 1)
]

answer_1 = (highest_trees.min(axis=2) < trees).sum()
print(f"answer 1 is {answer_1}")


def viewing_distance(row_of_trees: np.ndarray, value: int) -> int:
    w = np.where(row_of_trees >= value)[0]

    if not w.size:
        return len(row_of_trees)

    return w[0] + 1


# answer 2
v_distances = np.zeros(trees.shape + (4,), dtype=int)
v_distances[1:-1, 1:-1, :] = [
    [
        [
            viewing_distance(trees[i - 1 :: -1, j], trees[i, j]),
            viewing_distance(trees[i, j - 1 :: -1], trees[i, j]),
            viewing_distance(trees[i, j + 1 :], trees[i, j]),
            viewing_distance(trees[i + 1 :, j], trees[i, j]),
        ]
        for j in range(1, trees.shape[1] - 1)
    ]
    for i in range(1, trees.shape[0] - 1)
]
answer_2 = np.prod(v_distances, axis=2).max()
print(f"answer 2 is {answer_2}")
