from __future__ import annotations

import argparse
from functools import reduce
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
        self.max_height_in_direction = [None, None, None, None]   # up, down, left, right
        self.distance = [None, None, None, None]
        self.height = height

    def __repr__(self):
        return str(self.max_height_in_direction)

    def scenicValue(self):
        return reduce(lambda x, y: x* y, self.distance)

    def maxHeightFromDirection(self, direction):
        return self.max_height_in_direction[direction.value]

    def setMaxHeightFromDirection(self, direction, value, distance):
        self.max_height_in_direction[direction.value] = value
        self.distance[direction.value] = distance




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
        tree.max_height_in_direction = [float('inf'), float('inf'), float('inf'), float('inf')]
        tree.distance = [0,0,0,0]
    for tree in visible[-1]:
        tree.max_height_in_direction = [float('inf'), float('inf'), float('inf'), float('inf')]
        tree.distance = [0,0,0,0]

    for i in range(len(visible)):
        visible[i][0].max_height_in_direction = [float('inf'), float('inf'), float('inf'), float('inf')]
        visible[i][0].distance = [0,0,0,0]
        visible[i][-1].max_height_in_direction = [float('inf'), float('inf'), float('inf'), float('inf')]
        visible[i][-1].distance = [0,0,0,0]

    def checkVisibilityHelper(r, c, direction, needed_height):
        nr, nc = neighbors(r, c, direction)
        if nr < 0 or nr >= len(tree_heights) or nc < 0 or nc >= len(tree_heights[0]):
            return (float('inf'), 0)

        if visible[nr][nc].height >= needed_height:
            return (visible[nr][nc].height, 1)
        else:
            (height, distance) = checkVisibilityHelper(nr, nc, direction, needed_height)
            return (height, distance + 1)


    def checkVisibility(r, c, direction):
        # breakpoint()
        height, distance = checkVisibilityHelper(r, c, direction, visible[r][c].height)
        visible[r][c].setMaxHeightFromDirection(direction, height, distance)


    for r in range(len(visible)):
        for c in range(len(visible[r])):
            for direction in Direction:
                if visible[r][c].maxHeightFromDirection(direction) is None:
                    # breakpoint()
                    checkVisibility(r, c, direction)

    for r in tree_heights:
        print([elem for elem in r])

    for r in visible:
        print([elem.distance for elem in r])

    max_value = float('-inf')
    for r in visible:
        max_value = max(max_value, max([elem.scenicValue() for elem in r]))

    return max_value



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
        (INPUT_S, 8),
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
