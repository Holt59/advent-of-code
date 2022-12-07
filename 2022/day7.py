# -*- encoding: utf-8 -*-

import sys
from pathlib import Path

lines = sys.stdin.read().splitlines()

# we are going to use Path to create path and go up/down in the file tree since it
# implements everything we need
#
# we can use .resolve() to get normalized path, although this will add C:\ to all paths
# on Windows but that is not an issue since only the sizes matter
#

# mapping from path to list of files or directories
trees: dict[Path, list[Path]] = {}

# mapping from paths to either size (for file) or -1 for directory
sizes: dict[Path, int] = {}

# first line must be a cd otherwise we have no idea where we are
assert lines[0].startswith("$ cd")
base_path = Path(lines[0].strip("$").split()[1]).resolve()
cur_path = base_path

trees[cur_path] = []
sizes[cur_path] = -1

for line in lines[1:]:
    # command
    if line.startswith("$"):
        parts = line.strip("$").strip().split()
        command = parts[0]

        if command == "cd":
            cur_path = cur_path.joinpath(parts[1]).resolve()

            # just initialize the lis of files if not already done
            if cur_path not in trees:
                trees[cur_path] = []
        else:
            # nothing to do here
            pass

    # fill the current path
    else:
        parts = line.split()
        name: str = parts[1]
        if line.startswith("dir"):
            size = -1
        else:
            size = int(parts[0])

        path = cur_path.joinpath(name)
        trees[cur_path].append(path)
        sizes[path] = size


def compute_size(path: Path) -> int:
    size = sizes[path]

    if size >= 0:
        return size

    return sum(compute_size(sub) for sub in trees[path])


acc_sizes = {path: compute_size(path) for path in trees}

# part 1
answer_1 = sum(size for size in acc_sizes.values() if size <= 100_000)
print(f"answer 1 is {answer_1}")

# part 2
total_space = 70_000_000
update_space = 30_000_000
free_space = total_space - acc_sizes[base_path]

to_free_space = update_space - free_space

answer_2 = min(size for size in acc_sizes.values() if size >= to_free_space)
print(f"answer 2 is {answer_2}")
