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
            bag_info = bag.split()[:-1]
            if bag_info[0] == 'no':
                continue

            num_bags = int(bag_info[0])
            bag_name = " ".join(bag_info[1:])

            bags[container].append((num_bags, bag_name))

    check_bags = bags['shiny gold']
    total = 0

    while len(check_bags) != 0:
        num_bags, bag_type  = check_bags.pop(0)

        total += num_bags
        for contained_num, contained_bag_type in bags[bag_type]:
            check_bags.append((num_bags * contained_num, contained_bag_type))

    return total


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
INPUT2_S = '''\
shiny gold bags contain 2 dark red bags.
dark red bags contain 2 dark orange bags.
dark orange bags contain 2 dark yellow bags.
dark yellow bags contain 2 dark green bags.
dark green bags contain 2 dark blue bags.
dark blue bags contain 2 dark violet bags.
dark violet bags contain no other bags.
'''


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        (INPUT_S, 32),
        (INPUT2_S, 126),
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
