from __future__ import annotations

import argparse
import os.path
from xml.dom.pulldom import default_bufsize
from enum import Enum

import pytest

from support import timing

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

class Direction(Enum):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3

def neighbors(r, c, direction):
    match direction:
        case Direction.UP:
            return r-1, c
        case Direction.DOWN:
            return r+1, c
        case Direction.LEFT:
            return r, c - 1
        case Direction.RIGHT:
            return r, c + 1

class Visibility:
    def __init__(self, height):
        self.visible_direction = [None, None, None, None]   # up, down, left, right
        self.height = height

    def __repr__(self):
        return str(self.visible_direction)

    def isVisible(self):
        return any([val < self.height for val in self.visible_direction if val is not None])

    def maxHeightFromDirection(self, direction):
        return self.visible_direction[direction.value]

    def setMaxHeightFromDirection(self, direction, value):
        self.visible_direction[direction.value] = value



def compute(s: str) -> int:
    tree_heights = []
    lines = s.splitlines()
    for line in lines:
        tree_heights.append([int(char) for char in line])

    visible = [[None]*len(tree_heights[0]) for _ in range(len(tree_heights))]
    for r in range(len(visible)):
        for c in range(len(visible[r])):
            visible[r][c] = Visibility(tree_heights[r][c])
    # breakpoint()
    for tree in visible[0]:
        tree.setMaxHeightFromDirection(Direction.UP, float('-inf'))
    for tree in visible[-1]:
        tree.setMaxHeightFromDirection(Direction.DOWN, float('-inf'))

    for i in range(len(visible)):
        visible[i][0].setMaxHeightFromDirection(Direction.LEFT, float('-inf'))
        visible[i][-1].setMaxHeightFromDirection(Direction.RIGHT, float('-inf'))

    def checkVisibility(r, c, direction):
        if visible[r][c].maxHeightFromDirection(direction) is not None:
            return

        nr, nc = neighbors(r, c, direction)
        if nr < 0 or nr >= len(tree_heights) or nc < 0 or nc >= len(tree_heights[0]):
            return

        checkVisibility(nr, nc, direction)
        visible[r][c].setMaxHeightFromDirection(direction, max(visible[nr][nc].height, visible[nr][nc].maxHeightFromDirection(direction)))




    for r in range(len(visible)):
        for c in range(len(visible[r])):
            if not visible[r][c].isVisible():
                for direction in Direction:
                    # breakpoint()
                    checkVisibility(r, c, direction)
                    if visible[r][c].isVisible():
                        break

    for r in visible:
        print([elem.isVisible() for elem in r])

    count = 0
    for r in range(len(visible)):
        for c in range(len(visible[r])):
            if visible[r][c].isVisible():
                count += 1

    return count



INPUT_S = '''\
30373
25512
65332
33549
35390
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

    with open(args.data_file) as f, timing():
        print(compute(f.read()))

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
