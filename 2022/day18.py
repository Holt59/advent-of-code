# -*- encoding: utf-8 -*-

import sys
from typing import FrozenSet

import numpy as np

xyz = np.asarray(
    [
        tuple(int(x) for x in row.split(","))  # type: ignore
        for row in sys.stdin.read().splitlines()
    ]
)

xyz = xyz - xyz.min(axis=0) + 1

cubes = np.zeros(xyz.max(axis=0) + 3, dtype=bool)
cubes[xyz[:, 0], xyz[:, 1], xyz[:, 2]] = True

n_dims = len(cubes.shape)

faces = [(-1, 0, 0), (1, 0, 0), (0, -1, 0), (0, 1, 0), (0, 0, -1), (0, 0, 1)]

answer_1 = sum(
    1 for x, y, z in xyz for dx, dy, dz in faces if not cubes[x + dx, y + dy, z + dz]
)
print(f"answer 1 is {answer_1}")

visited = np.zeros_like(cubes, dtype=bool)
queue = [(0, 0, 0)]

n_faces = 0
while queue:
    x, y, z = queue.pop(0)

    if visited[x, y, z]:
        continue

    visited[x, y, z] = True

    for dx, dy, dz in faces:
        nx, ny, nz = x + dx, y + dy, z + dz
        if not all(n >= 0 and n < cubes.shape[i] for i, n in enumerate((nx, ny, nz))):
            continue

        if visited[nx, ny, nz]:
            continue

        if cubes[nx, ny, nz]:
            n_faces += 1
        else:
            queue.append((nx, ny, nz))
print(f"answer 2 is {n_faces}")
