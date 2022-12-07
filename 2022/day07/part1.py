from __future__ import annotations

import argparse
import os.path

import pytest

from support import timing

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

class FS:
    def __init__(self, name, parent = None, size = 0):
        self.children = {}
        self.parent = parent
        self.type = 0 if size == 0 else 1 # 0 is dir, 1 is file
        self.name = name
        self.size = size

    def __repr__(self):
        output = f"{self.name} has size {self.size}"
        if self.children:
            output += f"\n with children {self.children.values()}"

        return output

    def insert_child(self, name, size=0):
        # breakpoint()
        if self.type == 1:
            raise ValueError(f"Cannot insert child on file type {self.name}")

        if name in self.children:
            return self.children[name]

        child_node = FS(name, self, size)
        self.children[name] = child_node

        currNode = self
        while currNode != None:
            currNode.size += size
            currNode = currNode.parent

        return child_node


    def get_parent(self):
        return self.parent

    def get_part1(self):
        output = 0
        if self.size < 100000 and self.type == 0:
            output += self.size

        for _, child in self.children.items():
            output += child.get_part1()

        # print(f"{self.name} returning {output}")
        return output


def compute(s: str) -> int:

    lines = s.splitlines()
    rootNode = FS("dummy")
    currNode = rootNode
    # breakpoint()
    for line in lines:
        if "$" in line:
            _, action, *rest = line.split()
            if action == "cd":
                if rest[0] == "..":
                    currNode = currNode.get_parent()
                else:
                    currNode = currNode.insert_child(rest[0])
            elif action == "ls":
                continue
        else:
            value, name = line.split()
            if value == "dir":
                currNode.insert_child(name)
            else:
                currNode.insert_child(name, int(value))
        print(line)

    # TODO: implement solution here!
    return rootNode.get_part1()


INPUT_S = '''\
$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k
'''


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        (INPUT_S, 95437),
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
