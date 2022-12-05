from __future__ import annotations

import argparse
import os.path

import pytest

from support import timing
import re

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

def compute(s: str) -> int:
    front, rest = s.split("\n\n")

    front = front.splitlines()
    num_buckets = max([int(v) for v in front[-1].split()])
    buckets = [[] for _ in range(num_buckets)]
    for i, line in enumerate(front[:-1]):
        for j in range(0, len(line), 4):
            value = line[j:j+4].strip()
            bucket_index = j//4
            if value:
                buckets[bucket_index].append(value[1])

    for line in rest.splitlines():
        line = line.strip()
        if line:
            _, num_removed, _, start, _, end = line.split()
            num_removed, start, end = [int(v) for v in [num_removed, start, end]]
            start -= 1
            end -= 1

            removed_boxes = buckets[start][:num_removed]
            buckets[start] = buckets[start][num_removed:]
            buckets[end] = list(removed_boxes) + buckets[end]

    print(buckets)

    return "".join(bucket[0] if bucket else "" for bucket in buckets)


INPUT_S = '''\
    [D]
[N] [C]
[Z] [M] [P]
 1   2   3

move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2
'''


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        (INPUT_S, "MCD"),
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
