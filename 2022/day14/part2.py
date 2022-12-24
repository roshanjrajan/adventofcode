from __future__ import annotations

import argparse
import os.path

import pytest

from support import timing

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

SPACE = 200

def convert_index(left, right, bottom, coord):
    r, c = coord
    assert(left <= c <= right)
    assert(0 <= r <= bottom)

    return r, c - left

def compute(s: str) -> int:
    lines = s.splitlines()
    rock_patterns = []
    left, right, bottom = float('inf'), float('-inf'), float('-inf')
    for line in lines:
        curr_pattern = []
        coords = line.split(" -> ")
        for coord in coords:
            coord_col, coord_row = coord.split(",")
            coord_col, coord_row = int(coord_col), int(coord_row)
            left = min(left, coord_col)
            right = max(right, coord_col)
            bottom = max(bottom, coord_row)
            curr_pattern.append((coord_col, coord_row))
        rock_patterns.append(curr_pattern)

    left -= SPACE
    right += SPACE

    N_COLS = right - left + 1
    N_ROWS = bottom + 1 + 2

    arr = [[" "]*N_COLS for _ in range(N_ROWS)]
    arr[-1] =["#"]*N_COLS

    for rock_pattern in rock_patterns:
        prev = rock_pattern[0]

        for curr in rock_pattern[1:]:
            lower_col, upper_col = min(prev[0], curr[0]), max(prev[0], curr[0])
            lower_row, upper_row = min(prev[1], curr[1]), max(prev[1], curr[1])
            for r in range(lower_row, upper_row + 1):
                for c in range(lower_col, upper_col + 1):
                    cr, cc = convert_index(left, right, bottom, (r, c))
                    arr[cr][cc] = "#"
            prev = curr

    done = False
    sand_count = 0
    s_r, s_c = convert_index(left, right, bottom, (0, 500))
    while not done:
        c_r, c_c = s_r, s_c
        at_rest = False
        while not at_rest:
            if c_r + 1 < N_ROWS and arr[c_r + 1][c_c] == " ":
                c_r += 1
            elif c_r + 1 < N_ROWS and c_c - 1>= 0 and arr[c_r + 1][c_c - 1] == " ": # go left
                c_r += 1
                c_c -= 1
            elif c_r + 1 < N_ROWS and c_c + 1>= 0 and arr[c_r + 1][c_c + 1] == " ": # go right
                c_r += 1
                c_c += 1
            else:
                at_rest = True

        if s_r == c_r and s_c == c_c:
            return sand_count + 1

        arr[c_r][c_c] = "o"
        sand_count += 1
        # for row in arr:
        #     print("".join(row))
        # print(sand_count)
    # TODO: implement solution here!
    return -1


INPUT_S = '''\
498,4 -> 498,6 -> 496,6
503,4 -> 502,4 -> 502,9 -> 494,9
'''


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        (INPUT_S, 24),
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
