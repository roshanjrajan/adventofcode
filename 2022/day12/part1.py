from __future__ import annotations

import argparse
import os.path

import pytest

from support import timing

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

def neighbor(r, c):
    yield (r - 1, c)
    yield (r + 1, c)
    yield (r, c - 1)
    yield (r, c + 1)

def stringify(num):
    if num == 1:
        return "S"
    if num == 26:
        return "E"
    return chr(num + ord('a') - 1)

def char_value(ch):
    if ch == "S":
        return 0
    if ch == "E":
        return 27
    return ord(ch) - ord('a') + 1

def compute(s: str) -> int:

    lines = s.splitlines()
    N_ROWS, N_COLS = len(lines), len(lines[0])

    arr = [[char_value(ch) for ch in line] for line in lines]

    for r in range(len(arr)):
        for c in range(len(arr[r])):
            if arr[r][c] == 0:
                start_r, start_c = (r, c)
                arr[r][c] = 1
            if arr[r][c] == 27:
                end_r, end_c = (r, c)
                arr[r][c] = 26

    distance = [[float('inf')] * N_COLS for _ in range(N_ROWS)]
    queue = [((start_r, start_c), 0)]

    while queue:
        # breakpoint()
        (r, c), d = queue.pop(0)
        if distance[r][c] <= d:
            continue

        if r == end_r and  c == end_c:
            return d

        distance[r][c] = d
        for n_r, n_c in neighbor(r, c):
            if 0 <= n_r < N_ROWS and 0 <= n_c < N_COLS and (arr[n_r][n_c] <= arr[r][c] + 1):
                if d + 1 < distance[n_r][n_c]:
                    queue.append(((n_r, n_c), d + 1))

    return distance[end_r][end_c]


INPUT_S = '''\
Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi
'''


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        (INPUT_S, 31),
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
