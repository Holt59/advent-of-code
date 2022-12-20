# -*- encoding: utf-8 -*-

import sys


class Number:
    index: int
    current: int
    value: int

    def __init__(self, index: int, value: int):
        self.index = index
        self.current = index
        self.value = value

    def __eq__(self, other):
        if isinstance(other, Number):
            return self.value == other.value
        elif isinstance(other, int):
            return self.value == other
        return False

    def __hash__(self):
        return hash(self.index)

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return str(self)


def decrypt(numbers: list[Number], key: int, rounds: int) -> int:

    numbers = numbers.copy()
    original = numbers.copy()

    for number in numbers:
        number.current = number.index

    for _ in range(rounds):
        for number in original:
            index = number.current
            offset = (number.value * key) % (len(numbers) - 1)
            target = index + offset

            # need to wrap
            if target >= len(numbers):
                for number_2 in numbers[:index]:
                    number_2.current += 1
                numbers = [number] + numbers[:index] + numbers[index + 1 :]

                target = offset - (len(numbers) - index) + 1
                index = 0

            for number_2 in numbers[index : target + 1]:
                number_2.current -= 1

            number.current = target
            numbers = (
                numbers[:index]
                + numbers[index + 1 : target + 1]
                + [number]
                + numbers[target + 1 :]
            )

    index_of_0 = numbers.index(0)  # type: ignore
    return sum(
        numbers[(index_of_0 + offset) % len(numbers)].value * key
        for offset in (1000, 2000, 3000)
    )


numbers = [Number(i, int(x)) for i, x in enumerate(sys.stdin.readlines())]

answer_1 = decrypt(numbers, 1, 1)
print(f"answer 1 is {answer_1}")

answer_2 = decrypt(numbers, 811589153, 10)
print(f"answer 2 is {answer_2}")
