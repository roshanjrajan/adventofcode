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
    sum = 0
    for line in lines:
        p1, p2 = set(line[:len(line)//2]), (line[len(line)//2:])
        common = list(p1.intersection(p2))[0]
        # print(comm)
        if common > 'Z':
            value =  1 +  ord(common) - ord('a')
        else:
            value = 27 + ord(common) - ord('A')

        # print(common, value)
        sum += value

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
        (INPUT_S, 157),
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
