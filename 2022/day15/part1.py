from __future__ import annotations

import argparse
import os.path

import pytest
import re

from support import timing

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

def compute(s: str, ROW: int) -> int:

    lines = s.splitlines()
    intervals = []
    for line in lines:
        result = [int(d) for d in re.findall(r'-?\d+', line)]
        sx, sy, bx, by = result
        d = abs(sx - bx) + abs(sy - by)
        col_range = d - abs(sy - ROW)

        if col_range < 0:
            # print(f"Could not reach from {(sx, sy)} to ROW {ROW} as {(bx, by)} is too far")
            continue
        else:
            interval = (sx - col_range, sx + col_range)
            intervals.append(interval)

    intervals.sort()
    merged = []
    merged.append(intervals[0])
    for left, right in intervals[1:]:
        last_left, last_right = merged[-1]
        if last_left <= left <= last_right:
            merged[-1] = (last_left, max(last_right, right))
        else:
            merged.append((left, right))

    locs = 0
    for left, right in merged:
        locs += abs(right - left)

    return locs


INPUT_S = '''\
Sensor at x=2, y=18: closest beacon is at x=-2, y=15
Sensor at x=9, y=16: closest beacon is at x=10, y=16
Sensor at x=13, y=2: closest beacon is at x=15, y=3
Sensor at x=12, y=14: closest beacon is at x=10, y=16
Sensor at x=10, y=20: closest beacon is at x=10, y=16
Sensor at x=14, y=17: closest beacon is at x=10, y=16
Sensor at x=8, y=7: closest beacon is at x=2, y=10
Sensor at x=2, y=0: closest beacon is at x=2, y=10
Sensor at x=0, y=11: closest beacon is at x=2, y=10
Sensor at x=20, y=14: closest beacon is at x=25, y=17
Sensor at x=17, y=20: closest beacon is at x=21, y=22
Sensor at x=16, y=7: closest beacon is at x=15, y=3
Sensor at x=14, y=3: closest beacon is at x=15, y=3
Sensor at x=20, y=1: closest beacon is at x=15, y=3
'''


@pytest.mark.parametrize(
    ('input_s', 'row', 'expected'),
    (
        (INPUT_S, 10, 26),
    ),
)
def test(input_s: str, row: int, expected: int) -> None:
    assert compute(input_s, row) == expected


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('data_file', nargs='?', default=INPUT_TXT)
    args = parser.parse_args()

    with open(args.data_file) as f, timing():
        print(compute(f.read(), 2000000))

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
