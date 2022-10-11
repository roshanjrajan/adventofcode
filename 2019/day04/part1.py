from __future__ import annotations

import argparse
import os.path

import pytest

from support import timing

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

def contains_doubles(num: int) -> bool:
    num_str = str(num)

    for i in range(0, len(num_str) - 1):
        if num_str[i] == num_str[i + 1]:
            return True

    return False

def contains_increasing(num: int) -> bool:
    num_str = str(num)
    curr = num_str[0]

    for i in range(1, len(num_str)):
        if curr > num_str[i]:
            return False
        curr = num_str[i]

    return True



def compute(lower: int, higher: int) -> int:

    output = []
    for n in range(lower, higher):
        if contains_doubles(n) and contains_increasing(n):
            output.append(n)

    return len(output)


INPUT_S = '''\

'''


@pytest.mark.parametrize(
    ('lower', 'higher', 'expected'),
    (
        (0, 5, 1),
    ),
)
def test(lower: int, higher: int, expected: int) -> None:
    assert compute(lower, higher) == expected


def main() -> int:
    print(compute(147981,691423))

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
