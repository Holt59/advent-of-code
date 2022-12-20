# -*- encoding: utf-8 -*-

import sys


class Number:
    current: int
    value: int

    def __init__(self, value: int):
        self.current = 0
        self.value = value

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return str(self)


def decrypt(numbers: list[Number], key: int, rounds: int) -> int:

    numbers = numbers.copy()
    original = numbers.copy()

    for index, number in enumerate(numbers):
        number.current = index

    for _ in range(rounds):
        for number in original:
            index = number.current
            offset = (number.value * key) % (len(numbers) - 1)
            target = index + offset

            # need to wrap
            if target >= len(numbers):
                target = offset - (len(numbers) - index) + 1

                for number_2 in numbers[target:index]:
                    number_2.current += 1

                numbers = (
                    numbers[:target]
                    + [number]
                    + numbers[target:index]
                    + numbers[index + 1 :]
                )
            else:
                for number_2 in numbers[index : target + 1]:
                    number_2.current -= 1

                numbers = (
                    numbers[:index]
                    + numbers[index + 1 : target + 1]
                    + [number]
                    + numbers[target + 1 :]
                )
            number.current = target

    index_of_0 = next(
        filter(lambda index: numbers[index].value == 0, range(len(numbers)))
    )
    return sum(
        numbers[(index_of_0 + offset) % len(numbers)].value * key
        for offset in (1000, 2000, 3000)
    )


numbers = [Number(int(x)) for i, x in enumerate(sys.stdin.readlines())]

answer_1 = decrypt(numbers, 1, 1)
print(f"answer 1 is {answer_1}")

answer_2 = decrypt(numbers, 811589153, 10)
print(f"answer 2 is {answer_2}")
