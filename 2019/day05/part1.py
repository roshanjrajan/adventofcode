from __future__ import annotations

import argparse
import os.path
from site import addusersitepackages

import pytest

from support import timing

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

def get_parameter(mode: str, mem: List[int], loc : int) -> int:
    if mode == "0": # position_mode
        return mem[mem[loc]]
    elif mode == "1":
        return mem[loc]
    else:
        raise NotImplementedError(f"Parameter mode {mode} not implemented")


def compute(s: str) -> int:
    mem = [int(line) for line in s.splitlines()[0].split(",")]
    pc = 0
    input_value = 1

    while pc < len(mem):
        curr_instruction = str(mem[pc]).zfill(5)
        second_param_mode = curr_instruction[1]
        first_param_mode = curr_instruction[2]
        opcode = curr_instruction[3:]
        match opcode:
            case "01":
                val1 = get_parameter(first_param_mode, mem, pc + 1)
                val2 = get_parameter(second_param_mode, mem, pc + 2)
                address = mem[pc + 3]
                mem[address] = val1 + val2
                pc += 4
            case "02":
                val1 = get_parameter(first_param_mode, mem, pc + 1)
                val2 = get_parameter(second_param_mode, mem, pc + 2)
                address = mem[pc + 3]
                mem[address] = val1 * val2
                pc += 4
            case "03":
                mem[mem[pc + 1]] = input_value
                pc += 2
            case "04":
                print(mem[mem[pc + 1]])
                pc += 2
            case "99":
                return mem
            case _:
                raise AssertionError(f"Invalid pc {pc} - {curr_instruction} with mem {mem[pc-4: pc + 4]}")
        # breakpoint()
        pass
        # print(mem)


    # lines = s.splitlines()
    # for n in lines.split:
    #     pass
    # # TODO: implement solution here!
    raise AssertionError("The program never halts.")


INPUT_S = '''\
3,0,4,0,99
'''

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('data_file', nargs='?', default=INPUT_TXT)
    args = parser.parse_args()

    with open(args.data_file) as f, timing():
        print(compute(f.read()))

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
