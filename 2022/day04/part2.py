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
    overlaps = 0
    for line in lines:
        left, right = line.split(",")
        ll,lh = left.split("-")
        ll, lh = int(ll), int(lh)
        rl,rh = right.split("-")
        rl, rh = int(rl), int(rh)

        if ll <= rl and rh <= lh:
            overlaps += 1
            # print(ll, rl, rh, lh)
        elif rl <= ll and lh <= rh:
            overlaps += 1
            # print(rl, ll, lh , rh)
        elif ll <= rl <= lh <= rh:
            overlaps += 1
        elif rl <= ll <= rh <= lh:
            overlaps += 1

    return overlaps

    # TODO: implement solution here!
    return 0


INPUT_S = '''\
2-4,6-8
2-3,4-5
5-7,7-9
2-8,3-7
6-6,4-6
2-6,4-8
'''


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        (INPUT_S, 4),
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
