# -*- encoding: utf-8 -*-

import sys


class Number:
    index: int
    value: int

    def __init__(self, index: int, value: int):
        self.index = index
        self.value = value

    def __eq__(self, other):
        if isinstance(other, Number):
            return self.index == other.index
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
    numbers2index = {number: number.index for number in numbers}

    def swap(lhs: Number, rhs: Number):
        i1, i2 = numbers2index[lhs], numbers2index[rhs]
        numbers[i1], numbers[i2] = numbers[i2], numbers[i1]
        numbers2index[lhs], numbers2index[rhs] = i2, i1

    def move(index: int, value: int):
        assert value >= 0
        while value > 0:
            if index == len(numbers) - 1:
                swap(numbers[0], numbers[-1])
                index, value = 0, value - 1
            else:
                swap(numbers[index + 1], numbers[index])
                index, value = index + 1, value - 1

    for _ in range(rounds):
        for number in original:
            index = numbers2index[number]
            move(index, (number.value * key) % (len(numbers) - 1))

    index_of_0 = numbers.index(0)
    return sum(
        numbers[(index_of_0 + offset) % len(numbers)].value * key
        for offset in (1000, 2000, 3000)
    )


numbers = [Number(i, int(x)) for i, x in enumerate(sys.stdin.readlines())]

answer_1 = decrypt(numbers, 1, 1)
print(f"answer 1 is {answer_1}")

answer_2 = decrypt(numbers, 811589153, 10)
print(f"answer 2 is {answer_2}")
