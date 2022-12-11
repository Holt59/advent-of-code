# -*- encoding: utf-8 -*-

import copy
import sys
from functools import reduce
from typing import Callable, Final, Mapping, Sequence


class Monkey:

    id: Final[int]
    items: Final[Sequence[int]]
    worry_fn: Final[Callable[[int], int]]
    test_value: Final[int]
    throw_targets: Final[Mapping[bool, int]]

    def __init__(
        self,
        id: int,
        items: list[int],
        worry_fn: Callable[[int], int],
        test_value: int,
        throw_targets: dict[bool, int],
    ):
        self.id = id
        self.items = items
        self.worry_fn = worry_fn
        self.test_value = test_value
        self.throw_targets = throw_targets

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, Monkey):
            return False
        return self.id == o.id

    def __hash__(self) -> int:
        return hash(self.id)


def parse_monkey(lines: list[str]) -> Monkey:
    assert lines[0].startswith("Monkey")

    monkey_id = int(lines[0].split()[-1][:-1])

    # parse items
    items = [int(r.strip()) for r in lines[1].split(":")[1].split(",")]

    # parse worry
    worry_fn: Callable[[int], int]
    worry_s = lines[2].split("new =")[1].strip()
    operand = worry_s.split()[2].strip()

    if worry_s.startswith("old *"):
        if operand == "old":
            worry_fn = lambda w: w * w  # noqa: E731
        else:
            worry_fn = lambda w: w * int(operand)  # noqa: E731
    elif worry_s.startswith("old +"):
        if operand == "old":
            worry_fn = lambda w: w + w  # noqa: E731
        else:
            worry_fn = lambda w: w + int(operand)  # noqa: E731
    else:
        assert False, worry_s

    # parse test
    assert lines[3].split(":")[1].strip().startswith("divisible by")
    test_value = int(lines[3].split()[-1])

    assert lines[4].strip().startswith("If true")
    assert lines[5].strip().startswith("If false")
    throw_targets = {True: int(lines[4].split()[-1]), False: int(lines[5].split()[-1])}

    assert monkey_id not in throw_targets.values()

    return Monkey(monkey_id, items, worry_fn, test_value, throw_targets)


def run(
    monkeys: list[Monkey], n_rounds: int, me_worry_fn: Callable[[int], int]
) -> dict[Monkey, int]:
    """
    Perform a full run.

    Args:
        monkeys: Initial list of monkeys. The Monkey are not modified.
        n_rounds: Number of rounds to run.
        me_worry_fn: Worry function to apply after the Monkey operation (e.g., divide
            by 3 for round 1).

    Returns:
        A mapping containing, for each monkey, the number of items inspected.
    """
    # copy of the items
    items = {monkey: list(monkey.items) for monkey in monkeys}

    # number of inspects
    inspects = {monkey: 0 for monkey in monkeys}

    for round in range(n_rounds):

        for monkey in monkeys:
            for item in items[monkey]:
                inspects[monkey] += 1

                # compute the new worry level
                item = me_worry_fn(monkey.worry_fn(item))

                # find the target
                target = monkey.throw_targets[item % monkey.test_value == 0]
                assert target != monkey.id

                items[monkeys[target]].append(item)

            # clear after the loop
            items[monkey].clear()

    return inspects


def monkey_business(inspects: dict[Monkey, int]) -> int:
    sorted_levels = sorted(inspects.values())
    return sorted_levels[-2] * sorted_levels[-1]


monkeys = [parse_monkey(block.splitlines()) for block in sys.stdin.read().split("\n\n")]

# case 1: we simply divide the worry by 3 after applying the monkey worry operation
answer_1 = monkey_business(
    run(copy.deepcopy(monkeys), 20, me_worry_fn=lambda w: w // 3)
)
print(f"answer 1 is {answer_1}")

# case 2: to keep reasonable level values, we can use a modulo operation, we need to
# use the product of all "divisible by" test so that the test remains valid
#
# (a + b) % c == ((a % c) + (b % c)) % c --- this would work for a single test value
#
# (a + b) % c == ((a % d) + (b % d)) % c --- if d is a multiple of c, which is why here
# we use the product of all test value
#
total_test_value = reduce(lambda w, m: w * m.test_value, monkeys, 1)
answer_2 = monkey_business(
    run(copy.deepcopy(monkeys), 10_000, me_worry_fn=lambda w: w % total_test_value)
)
print(f"answer 2 is {answer_2}")
