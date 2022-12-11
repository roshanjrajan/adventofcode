from __future__ import annotations

import argparse
import os.path

import pytest

from support import timing

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

# class Array():
#     def __init__(self, items):
#         self.array = items
#         self.tail = len(items)

#     def append(self, value):
#         if self.tail == len(self.array):
#             self.array = self.array + [0] * 10

#         self.array[self.tail] = value
#         self.tail += 1

#     def clear(self):
#         for i in range(self.tail):
#             self.array[i] = 0
#         self.tail = 0

class Monkey():
    def __init__(self, items, op_and_operand, test, true_index, false_index):
        self.items = items
        self.op_and_operand = op_and_operand
        self.test = test
        self.true_index = true_index
        self.false_index = false_index
        self.inspection_count = 0
        self.max_test = None

    def __repr__(self):
        return f"Monkey({self.items}, {self.op_and_operand}, {self.test}, {self.true_index}, {self.false_index}, {self.inspection_count})"

    def do_op(self, item):
        op, operand = self.op_and_operand
        if operand == "old":
            operand = item
        else:
            operand = int(operand)

        if op == '+':
            return item + operand
        elif op == '*':
            return item * operand
        elif op == '-':
            return item - operand
        elif op == '/':
            return item // operand
        else:
            raise ValueError(f"Invalid OP {self.op_and_operand}")

    def check(self, monkeys, max_test):
        for item in self.items:
            worry_level = self.do_op(item)
            worry_level = worry_level % max_test
            if worry_level % self.test == 0:
                monkeys[self.true_index].items.append(worry_level)
            else:
                monkeys[self.false_index].items.append(worry_level)
        self.inspection_count += len(self.items)
        self.items = []


def compute(s: str) -> int:
    monkeys = []
    monkeys_info = s.split("\n\n")
    max_test = 1
    for monkey_info in monkeys_info:
        monkey_info = monkey_info.split("\n")
        monkey_items = [int(item) for item in monkey_info[1].split(":")[1].split(",")]
        monkey_op_and_operand = monkey_info[2].split("old ")[1].split(" ")
        monkey_test = int(monkey_info[3].split("divisible by")[1])
        monkey_true_index = int(monkey_info[4].split("throw to monkey")[1])
        monkey_false_index = int(monkey_info[5].split("throw to monkey")[1])
        monkeys.append(Monkey(monkey_items, monkey_op_and_operand, monkey_test, monkey_true_index, monkey_false_index))
        max_test *= monkey_test

    print(max_test)

    print(len(monkeys))
    for i in range(10000):
        for monkey in monkeys:
            monkey.check(monkeys, max_test)

    inspection_count = []
    for monkey in monkeys:
        inspection_count.append(monkey.inspection_count)

    inspection_count.sort(reverse=True)

    # TODO: implement solution here!
    return inspection_count[0] * inspection_count[1]


INPUT_S = '''\
Monkey 0:
  Starting items: 79, 98
  Operation: new = old * 19
  Test: divisible by 23
    If true: throw to monkey 2
    If false: throw to monkey 3

Monkey 1:
  Starting items: 54, 65, 75, 74
  Operation: new = old + 6
  Test: divisible by 19
    If true: throw to monkey 2
    If false: throw to monkey 0

Monkey 2:
  Starting items: 79, 60, 97
  Operation: new = old * old
  Test: divisible by 13
    If true: throw to monkey 1
    If false: throw to monkey 3

Monkey 3:
  Starting items: 74
  Operation: new = old + 3
  Test: divisible by 17
    If true: throw to monkey 0
    If false: throw to monkey 1
'''


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        (INPUT_S, 2713310158),
    ),
)
def test(input_s: str, expected: int) -> None:
    assert compute(input_s) == expected


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('data_file', nargs='?', default=INPUT_TXT)
    args = parser.parse_args()

    with open(args.data_file) as f, timing():
        print(compute(f.read()))

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
