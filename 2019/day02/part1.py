from __future__ import annotations

import argparse
import os.path

import pytest

from support import timing

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str) -> int:
    mem = [int(line) for line in s.splitlines()[0].split(",")]
    pc = 0

    while pc < len(mem):
        # breakpoint()
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
        # print(mem)


    # lines = s.splitlines()
    # for n in lines.split:
    #     pass
    # # TODO: implement solution here!
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
