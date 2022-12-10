from __future__ import annotations

import argparse
import os.path

import pytest

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

class GpsTree():
    def __init__(self):
        self.left = None
        self.right = None
        self.kids = []

    def add_child(self, path, child_name):
        if len(path) == 0:
            self.kids.append(child_name)
            return

        if path[0] == 'L':
            if self.left is None:
                self.left = GpsTree()
            self.left.add_child(path[1:], child_name)
        else:
            if self.right is None:
                self.right = GpsTree()
            self.right.add_child(path[1:], child_name)

    def collapse(self):
        if self.kids:
            if self.left:
                self.left.collapse()
            if self.right:
                self.right.collapse()
        elif self.left is None and self.right is not None:
            self.kids = self.right.kids
            self.left = self.right.left
            self.right = self.right.right
            self.collapse()
        elif self.right is None and self.left is not None:
            self.kids = self.left.kids
            self.right = self.left.right
            self.left = self.left.left
            self.collapse()
        else:
            if self.left:
                self.left.collapse()
            if self.right:
                self.right.collapse()

def find_closest_kid_helper(self, curr_node, distance):
    if curr_node is None:
        return None, float('inf')

    if curr_node.kids:
        return curr_node.kids[0], distance
    else:
        left_kid, left_dist = find_closest_kid_helper(self, curr_node.left, distance + 1)
        right_kid, right_dist = find_closest_kid_helper(self, curr_node.right, distance + 1)
        if right_dist < left_dist:
            return right_kid, right_dist
        else:
            return left_kid, left_dist

def find_closest_kid(curr_node):
    if curr_node.kids:
        return curr_node.kids[0]
    else:
        kid, _ = find_closest_kid_helper(curr_node, curr_node, 0)
        return kid


def compute(s: str) -> int:
    root = GpsTree()
    lines = s.splitlines()
    for line in lines:
        child_name, path = line.split(' - ')
        path.strip()
        child_name.strip()
        root.add_child(path, child_name)

    root.collapse()
    name = find_closest_kid(root)
    # TODO: implement solution here!
    return name


INPUT_S = '''\
tamo - RLRLR
loic - RLLL
kero - LRLR
luna - LRRR
caro - LRL
lena - RLLR
thomas - LRLL
tommy - LLL
chayaline - LRLL
'''


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        (INPUT_S, "tommy"),
    ),
)
def test(input_s: str, expected: int) -> None:
    assert compute(input_s) == expected


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('data_file', nargs='?', default=INPUT_TXT)
    args = parser.parse_args()

    with open(args.data_file) as f:
        print(compute(f.read()))

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
