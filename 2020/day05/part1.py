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
    highest = 0
    for line in lines:
        row_range = (0, 127)
        col_range = (0, 7)
        for char in line:
            if char == 'F':
                row_range = (row_range[0], (row_range[0] + row_range[1])//2)
            elif char == 'B':
                row_range = ((row_range[0] + row_range[1] + 1)//2, row_range[1])
            elif char == 'L':
                col_range = (col_range[0], (col_range[0] + col_range[1])//2)
            elif char == 'R':
                col_range = ((col_range[0] + col_range[1] + 1)//2, col_range[1])

        highest = max(highest, row_range[0] * 8 + col_range[0])
    return highest


INPUT_S = '''\
FBFBBFFRLR
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
