from __future__ import annotations

import argparse
from ctypes.wintypes import HACCEL
import os.path

import pytest

from support import timing

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

def update_rope(ropes, direction):
    match direction:
        case "U":
            ropes[0] = (ropes[0][0] + 1, ropes[0][1])
        case "D":
            ropes[0] = (ropes[0][0] - 1, ropes[0][1])
        case "L":
            ropes[0] = (ropes[0][0], ropes[0][1] - 1)
        case "R":
            ropes[0] = (ropes[0][0], ropes[0][1] + 1)

    for i in range(1, len(ropes)):
        if ropes[i-1][0] == ropes[i][0] + 2 and ropes[i-1][1] == ropes[i][1]:
            ropes[i] = (ropes[i][0] + 1, ropes[i][1])
        elif ropes[i-1][0] == ropes[i][0] - 2 and ropes[i-1][1] == ropes[i][1]:
            ropes[i] = (ropes[i][0] - 1, ropes[i][1])
        elif ropes[i-1][1] == ropes[i][1] + 2 and ropes[i-1][0] == ropes[i][0]:
            ropes[i] = (ropes[i][0], ropes[i][1] + 1)
        elif ropes[i-1][1] == ropes[i][1] - 2 and ropes[i-1][0] == ropes[i][0]:
            ropes[i] = (ropes[i][0], ropes[i][1] - 1)
        elif ropes[i-1][0] == ropes[i][0] + 2 and ropes[i-1][1] > ropes[i][1]:
            ropes[i] = (ropes[i][0] + 1, ropes[i][1] + 1)
        elif ropes[i-1][0] == ropes[i][0] + 2 and ropes[i-1][1] < ropes[i][1]:
            ropes[i] = (ropes[i][0] + 1, ropes[i][1] - 1)
        elif ropes[i-1][0] == ropes[i][0] - 2 and ropes[i-1][1] > ropes[i][1]:
            ropes[i] = (ropes[i][0] - 1, ropes[i][1] + 1)
        elif ropes[i-1][0] == ropes[i][0] - 2 and ropes[i-1][1] < ropes[i][1]:
            ropes[i] = (ropes[i][0] - 1, ropes[i][1] - 1)
        elif ropes[i-1][1] == ropes[i][1] + 2 and ropes[i-1][0] > ropes[i][0]:
            ropes[i] = (ropes[i][0] + 1, ropes[i][1] + 1)
        elif ropes[i-1][1] == ropes[i][1] + 2 and ropes[i-1][0] < ropes[i][0]:
            ropes[i] = (ropes[i][0] - 1, ropes[i][1] + 1)
        elif ropes[i-1][1] == ropes[i][1] - 2 and ropes[i-1][0] > ropes[i][0]:
            ropes[i] = (ropes[i][0] + 1, ropes[i][1] - 1)
        elif ropes[i-1][1] == ropes[i][1] - 2 and ropes[i-1][0] < ropes[i][0]:
            ropes[i] = (ropes[i][0] - 1, ropes[i][1] - 1)

    return ropes[-1]


def compute(s: str) -> int:
    visited = set()
    ropes = [(0, 0)]*10

    lines = s.splitlines()
    for line in lines:
        direction, distance = line.split()
        distance = int(distance)
        for i in range(distance):
            last_val = update_rope(ropes, direction)
            visited.add(last_val)
    return len(visited)


INPUT_S = '''\
R 5
U 8
L 8
D 3
R 17
D 10
L 25
U 20
'''


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        (INPUT_S, 0),
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
