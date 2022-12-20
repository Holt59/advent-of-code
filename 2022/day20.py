# -*- encoding: utf-8 -*-

import math
import sys


class Number:
    processed: bool
    value: int

    def __init__(self, value: int):
        self.value = value
        self.processed = False

    def __eq__(self, other):
        if isinstance(other, Number):
            return self.value == other.value
        elif isinstance(other, int):
            return self.value == other
        return False

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return str(self)


expected = iter(
    [
        [1, 2, -3, 3, -2, 0, 4],
        [2, 1, -3, 3, -2, 0, 4],
        [1, -3, 2, 3, -2, 0, 4],
        [1, 2, 3, -2, -3, 0, 4],
        [1, 2, -2, -3, 0, 3, 4],
        [1, 2, -3, 0, 3, 4, -2],
        [1, 2, -3, 0, 3, 4, -2],
        [1, 2, -3, 4, 0, 3, -2],
    ]
)


numbers = [Number(int(x)) for x in sys.stdin.readlines()]
# numbers = [Number(0), Number(0), Number(-6)]

# print(next(expected))
# print(numbers)
# print("---")

index = 0
while index < len(numbers):
    if numbers[index].processed:
        index += 1
        continue

    number = numbers[index]
    number.processed = True
    target = (
        index
        + (number.value % len(numbers))
        - int(number.value < 0) * math.ceil(abs(number.value) / len(numbers))
    ) % len(numbers)

    # print(
    #     f"moving {number} from {index} to {target} (between {numbers[target]} and {numbers[(target + 1) % len(numbers)]})"
    # )
    if target == index:
        index += 1
    elif target == index + 1:
        numbers[index], numbers[target] = numbers[target], numbers[index]
    elif target == index - 1:
        numbers[index], numbers[target] = numbers[target], numbers[index]
    elif target > index:
        # print(
        #     numbers[:index],
        #     numbers[index + 1 : target + 1],
        #     [numbers[index]],
        #     numbers[target + 1 :],
        # )
        numbers = (
            numbers[:index]
            + numbers[index + 1 : target + 1]
            + [numbers[index]]
            + numbers[target + 1 :]
        )
    else:
        numbers = (
            numbers[: target + 1]
            + [numbers[index]]
            + numbers[target + 1 : index]
            + numbers[index + 1 :]
        )
        index -= 1

    # print(next(expected))
    # print(numbers)
    # print("---")

index_of_0 = numbers.index(Number(0))

answer_1 = sum(
    numbers[(index_of_0 + offset) % len(numbers)].value for offset in (1000, 2000, 3000)
)
print(f"answer 1 is {answer_1}")
