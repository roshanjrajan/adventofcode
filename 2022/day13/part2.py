from __future__ import annotations

import argparse
import os.path

import pytest

from support import timing
import functools

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')
nothing = '''
When comparing two values, the first value is called left and the second value is called right. Then:

If both values are integers, the lower integer should come first.
If the left integer is lower than the right integer, the inputs are in the right order.
If the left integer is higher than the right integer, the inputs are not in the right order.
Otherwise, the inputs are the same integer; continue checking the next part of the input.

If both values are lists, compare the first value of each list, then the second value, and so on.
If the left list runs out of items first, the inputs are in the right order.
'If the right list runs out of items first, the inputs are not in the right order.
If the lists are the same length and no comparison makes a decision about the order, continue checking the next part of the input.

If exactly one value is an integer,
convert the integer to a list which contains that integer as its only value, then retry the comparison.
For example, if comparing [0,0,0] and 2,
convert the right value to [2] (a list containing 2);
the result is then found by instead comparing [0,0,0] and [2].
'''
def compare(left, right):
    if isinstance(left, int) and isinstance(right, int):
        if left < right:
            return -1
        elif left == right:
            return 0
        else:
            return 1
    elif isinstance(left, list) and isinstance(right, list):
        for i, item in enumerate(left):
            if i >= len(right):
                return 1

            comparison = compare(item, right[i])
            if comparison != 0:
                return comparison

        if len(left) < len(right):
            return -1

        return 0
    else:
        if not isinstance(left, list):
            left = [left]

        if not isinstance(right, list):
            right = [right]

        return compare(left, right)


def compute(s: str) -> int:
    packets = s.split("\n\n")
    correct_order = 0
    all_packets = []
    for i, packet in enumerate(packets):
        packet = packet.strip()
        left, right = packet.split("\n")
        left = eval(left)
        right = eval(right)
        all_packets.append(left)
        all_packets.append(right)

    all_packets.append([[2]])
    all_packets.append([[6]])
    sorted_packets = sorted(all_packets, key=functools.cmp_to_key(compare))

    for i, packet in enumerate(sorted_packets):
        if packet == [[2]]:
            index = i + 1
        elif packet == [[6]]:
            index2 = i + 1

    return index * index2


INPUT_S = '''\
[1,1,3,1,1]
[1,1,5,1,1]

[[1],[2,3,4]]
[[1],4]

[9]
[[8,7,6]]

[[4,4],4,4]
[[4,4],4,4,4]

[7,7,7,7]
[7,7,7]

[]
[3]

[[[]]]
[[]]

[1,[2,[3,[4,[5,6,7]]]],8,9]
[1,[2,[3,[4,[5,6,0]]]],8,9]
'''


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        (INPUT_S, 140),
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
