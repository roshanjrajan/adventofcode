from __future__ import annotations

import argparse
import os.path

import pytest

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

class GpsTree():
    def __init__(self, parent = None):
        self.left = None
        self.right = None
        self.kids = []
        self.parent = parent
        self.done = False

    def add_child(self, path, child_name):
        if len(path) == 0:
            self.kids.append(child_name)
            return

        if path[0] == 'L':
            if self.left is None:
                self.left = GpsTree(self)
            self.left.add_child(path[1:], child_name)
        else:
            if self.right is None:
                self.right = GpsTree(self)
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
            self.right = self.right.right # must be last
            self.collapse()
        elif self.right is None and self.left is not None:
            self.kids = self.left.kids
            self.right = self.left.right
            self.left = self.left.left # must be last
            self.collapse()
        else:
            if self.left:
                self.left.collapse()
            if self.right:
                self.right.collapse()

def get_total_steps(root, num_children):
    children_left = num_children
    curr_root = root
    total_distance = 0
    while children_left > 0:
        visited = set()
        queue = [(curr_root, 0)]
        while queue:
            curr_node, distance = queue.pop(0)
            if curr_node is None or curr_node in visited:
                continue

            visited.add(curr_node)

            if not curr_node.done and curr_node.kids:
                curr_node.done = True
                total_distance += distance
                children_left -= len(curr_node.kids)
                curr_root = curr_node
                # breakpoint()
                break
            else:
                queue.append((curr_node.left, distance + 1))
                queue.append((curr_node.right, distance + 1))
                queue.append((curr_node.parent, distance + 1))


    return total_distance


def compute(s: str) -> int:
    root = GpsTree()
    lines = s.splitlines()
    num_children = len(lines)
    for line in lines:
        child_name, path = line.split(' - ')
        path.strip()
        child_name.strip()
        root.add_child(path, child_name)

    root.collapse()
    return get_total_steps(root, num_children)


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
        (INPUT_S, 21),
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
