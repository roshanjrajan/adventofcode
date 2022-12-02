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

    choice_map = {
        "X": "A",
        "Y": "B",
        "Z": "C",
    }

    value = {
        "A": 1,
        "B" : 2,
        "C" : 3
    }

    score = 0
    lines = s.splitlines()
    for line in lines:
        opp, choice = line.split()
        if choice_map[choice] == win[opp]:
            score += value[choice_map[choice]] + 6
        elif choice_map[choice] == opp:
            score += value[choice_map[choice]] + 3
        else:
            score += value[choice_map[choice]]

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
        (INPUT_S, 15),
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
