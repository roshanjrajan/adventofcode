from __future__ import annotations

import argparse
import os.path

import pytest

from support import timing

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str) -> int:
    # numbers = [int(line) for line in s.splitlines()]
    # for n in numbers:
    #     pass

    orig_data = s.splitlines()
    count = 0
    changed_instr = 0
    found = False
    while not found:
        curr_run = list(orig_data)

        for i, instr in enumerate(curr_run[changed_instr + 1:]):
            op, val = instr.split()
            if op == "nop":
                curr_run[i] = "jmp " + val
                changed_instr = i
                break
            elif op == "jmp":
                curr_run[i] = "nop " + val
                changed_instr = i
                break

        print(count)
        touched = [False] * len(curr_run)
        curr_instr = 0
        acc = 0
        while touched[curr_instr] == False:
            touched[curr_instr] = True
            op, val = curr_run[curr_instr].split()
            print(f"{curr_instr=} - {op} {val}")
            if op == 'acc':
                acc += int(val)
                curr_instr += 1
            elif op == 'jmp':
                curr_instr += int(val)
            elif op == 'nop':
                curr_instr += 1

            if curr_instr >= len(curr_run):
                found = True
                break
        count += 1
        break

    return acc


INPUT_S = '''\
nop +0
acc +1
jmp +4
acc +3
jmp -3
acc -99
acc +1
jmp -4
acc +6
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
