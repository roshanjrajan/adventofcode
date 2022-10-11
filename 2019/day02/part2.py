from __future__ import annotations
from typing import List

import argparse
import os.path

import pytest

from support import timing

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

def run_program(mem: List[int]) -> int:
    pc = 0

    while pc < len(mem):
        match mem[pc]:
            case 1:
                val1 = mem[mem[pc + 1]]
                val2 = mem[mem[pc + 2]]
                mem[mem[pc + 3]] = val1 + val2
            case 2:
                val1 = mem[mem[pc + 1]]
                val2 = mem[mem[pc + 2]]
                mem[mem[pc + 3]] = val1 * val2
            case 99:
                return mem[0]
            case _:
                print(f"Invalid pc {pc}")

        pc += 4
    return mem[0]


def compute(s: str) -> int:
    mem = [int(line) for line in s.splitlines()[0].split(",")]

    for noun in range(100):
        for verb in range(100):
            prog_mem = list(mem)
            prog_mem[1] = noun
            prog_mem[2] = verb

            if run_program(prog_mem) == 19690720:
                return 100 * noun + verb

    raise AssertionError("The program never halts.")


INPUT_S = '''\
1,9,10,3,2,3,11,0,99,30,40,50
'''


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        (INPUT_S, 3500),
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
