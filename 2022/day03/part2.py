from __future__ import annotations

import argparse
import os.path

import pytest

from support import timing

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str) -> int:
    # numbers = [int(line) for line in s.splitlines()]
    # for n in numbers:
    #     pass

    lines = s.splitlines()
    rucksack = []
    sum = 0
    for line in lines:
        rucksack.append(set(line))
        if len(rucksack) == 3:
            common = list((rucksack[0].intersection(rucksack[1])).intersection(rucksack[2]))[0]

            if common > 'Z':
                value =  1 +  ord(common) - ord('a')
            else:
                value = 27 + ord(common) - ord('A')
            # print(common, value)
            sum += value
            rucksack = []

    return sum


INPUT_S = '''\
vJrwpWtwJgWrhcsFMMfFFhFp
jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
PmmdzqPrVvPwwTWBwg
wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
ttgJtRGJQctTZtZT
CrZsJsPPZsGzwwsLwLmpwMDw
'''


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        (INPUT_S, 70),
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
