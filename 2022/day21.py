# -*- encoding: utf-8 -*-

import operator
import sys
from typing import Callable


def compute(monkeys: dict[str, int | tuple[str, str, str]], monkey: str) -> int:
    value = monkeys[monkey]
    if isinstance(value, int):
        return value
    else:
        op: dict[str, Callable[[int, int], int]] = {
            "+": operator.add,
            "-": operator.sub,
            "*": operator.mul,
            "/": operator.floordiv,
        }
        value = op[value[1]](compute(monkeys, value[0]), compute(monkeys, value[2]))
        monkeys[monkey] = value
        return value


def invert(
    monkeys: dict[str, int | tuple[str, str, str]], monkey: str, target: int
) -> dict[str, int | tuple[str, str, str]]:
    """
    Revert the given mapping from monkey name to value or operation such that
    the value from 'monkey' is computable by inverting operation until the root is
    found.

    Args:
        monkeys: Dictionary of monkeys, that will be updated and returned.
        monkey: Name of the monkey to start from.
        target: Target value to set for the monkey that depends on root.

    Returns:
        The given dictionary of monkeys.
    """

    monkeys = monkeys.copy()

    depends: dict[str, str] = {}
    for m, v in monkeys.items():
        if isinstance(v, int):
            continue

        op1, _, op2 = v

        assert op1 not in depends
        assert op2 not in depends
        depends[op1] = m
        depends[op2] = m

    invert_op = {"+": "-", "-": "+", "*": "/", "/": "*"}

    current = monkey
    while True:
        dep = depends[current]

        if dep == "root":
            monkeys[current] = target
            break

        val = monkeys[dep]
        assert not isinstance(val, int)

        op1, ope, op2 = val

        if op1 == current:
            monkeys[current] = (dep, invert_op[ope], op2)
        elif ope in ("+", "*"):
            monkeys[current] = (dep, invert_op[ope], op1)
        else:
            monkeys[current] = (op1, ope, dep)

        current = dep

    return monkeys


lines = sys.stdin.read().splitlines()

monkeys: dict[str, int | tuple[str, str, str]] = {}

op_monkeys: set[str] = set()

for line in lines:
    parts = line.split(":")
    name = parts[0].strip()

    try:
        value = int(parts[1].strip())
        monkeys[name] = value
    except ValueError:
        op1, ope, op2 = parts[1].strip().split()
        monkeys[name] = (op1, ope, op2)

        op_monkeys.add(name)


answer_1 = compute(monkeys.copy(), "root")
print(f"answer 1 is {answer_1}")

# assume the second operand of 'root' can be computed, and the first one depends on
# humn, which is the case is my input and the test input
p1, _, p2 = monkeys["root"]  # type: ignore
answer_2 = compute(invert(monkeys, "humn", compute(monkeys.copy(), p2)), "humn")
print(f"answer 2 is {answer_2}")
