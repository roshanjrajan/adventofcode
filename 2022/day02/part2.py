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

    win = {
        "A": "B",
        "B" : "C",
        "C" : "A"
    }

    lose = {value : key for key, value in win.items()}

    value = {
        "A": 1,
        "B" : 2,
        "C" : 3
    }

    score = 0
    lines = s.splitlines()
    for line in lines:
        opp, strategy = line.split()
        match strategy:
            case "Z":
                score += value[win[opp]] + 6
            case "Y":
                score += value[opp] + 3
            case "X":
                score += value[lose[opp]]
            case default:
                raise AssertionError("invalid")

    # TODO: implement solution here!
    return score


INPUT_S = '''\
A Y
B X
C Z
'''


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        (INPUT_S, 12),
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
