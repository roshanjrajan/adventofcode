from __future__ import annotations

import argparse
from collections import defaultdict
import os.path

import pytest

from support import timing

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str) -> int:
    # numbers = [int(line) for line in s.splitlines()]
    # for n in numbers:
    #     pass

    lines = s.splitlines()
    group_answers = defaultdict(int)
    unique_answers = 0
    num_in_group = 0
    for line in lines:
        if not line:
            for answer in group_answers:
                unique_answers += 1 if group_answers[answer] == num_in_group else 0
            group_answers = defaultdict(int)
            num_in_group = 0
        else:
            num_in_group += 1
            for char in line:
                group_answers[char] += 1

    for answer in group_answers:
        unique_answers += 1 if group_answers[answer] == num_in_group else 0
    return unique_answers


INPUT_S = '''\
abc

a
b
c

ab
ac

a
a
a
a

b
'''


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        (INPUT_S, 1),
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
