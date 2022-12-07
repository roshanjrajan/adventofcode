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

    line = s.splitlines()[0]
    end = 4
    while end < len(line):
        window = line[end-4:end]
        # print(list(set(window)), window, end)
        if len(list(set(window))) == len(window):
            return end
        end += 1
    # TODO: implement solution here!
    return -1


INPUT_S = '''\

'''


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        ("mjqjpqmgbljsphdztnvjfqwrcgsmlb", 7),
        ("bvwbjplbgvbhsrlpgdmjqwftvncz", 5),
        ("nppdvjthqldpwncqszvftbrmjlhg", 6),
        ("nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg", 10),
        ("zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw", 11),
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
