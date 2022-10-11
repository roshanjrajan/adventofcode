from __future__ import annotations

import argparse
import os.path

import pytest

from support import timing

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

def calc_fuel(n: int) -> int:
    if n <= 6:
        return 0

    result = n // 3 - 2
    return result + calc_fuel(result)

def compute(s: str) -> int:
    numbers = [int(line) for line in s.splitlines()]
    sum = 0
    for n in numbers:
        sum += calc_fuel(n)


    # lines = s.splitlines()
    # for line in lines:
    #     pass
    # # TODO: implement solution here!
    # return 0

    return sum


INPUT_S = '''\

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
