from __future__ import annotations

import argparse
from collections import defaultdict
import os.path

import pytest

from support import timing

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str) -> int:
    # numbers = [int(line) for line in s.splitlines()]
    # for n in numbers:
    #     pass

    lines = s.splitlines()
    bags = defaultdict(list)

    for line in lines:
        container, contains = line.split(' contain ')
        container = " ".join(container.split()[:-1])

        contained_bags = contains.split(',')

        for bag in contained_bags:
            bag = " ".join(bag.split()[1:-1])

            bags[bag].append(container)

    check_bags = bags['shiny gold']
    all_bags = set()

    while len(check_bags) != 0:
        bag  = check_bags.pop(0)
        if bag not in all_bags:
            check_bags += bags[bag]
            all_bags.add(bag)

    return len(all_bags)


INPUT_S = '''\
light red bags contain 1 bright white bag, 2 muted yellow bags.
dark orange bags contain 3 bright white bags, 4 muted yellow bags.
bright white bags contain 1 shiny gold bag.
muted yellow bags contain 2 shiny gold bags, 9 faded blue bags.
shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.
dark olive bags contain 3 faded blue bags, 4 dotted black bags.
vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.
faded blue bags contain no other bags.
dotted black bags contain no other bags.
'''


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        (INPUT_S, 5),
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
