import re
import os
from pprint import pprint


def get_combo_operand_value(operand, a, b, c):
    if operand < 4:
        return operand
    if operand == 4:
        return a
    if operand == 5:
        return b
    if operand == 6:
        return c
    raise


with open(os.path.join(os.path.dirname(__file__), "input.txt")) as f:
    lines = f.readlines()

a = 0
b = 0
c = 0
program = []
for line in lines:
    reg_a = re.match(r"Register A: (\d+)", line)
    if reg_a is not None:
        a = int(reg_a.groups()[0])
        continue

    reg_b = re.match(r"Register B: (\d+)", line)
    if reg_b is not None:
        b = int(reg_b.groups()[0])
        continue

    reg_c = re.match(r"Register C: (\d+)", line)
    if reg_c is not None:
        c = int(reg_c.groups()[0])
        continue

    if "Program:" in line:
        program = [int(x) for x in line.strip().split(' ')[1].split(',')]
        break

output = []
instruction_pointer = 0
while instruction_pointer < len(program) - 1:
    opcode = program[instruction_pointer]
    operand = program[instruction_pointer + 1]

    if opcode == 0:
        # adv
        numerator = a
        denominator = 2 ** get_combo_operand_value(operand, a, b, c)
        a = numerator // denominator
    elif opcode == 1:
        # bxl
        b = b ^ operand
    elif opcode == 2:
        # bst
        b = get_combo_operand_value(operand, a, b, c) % 8
    elif opcode == 3:
        # jnz
        if a != 0:
            instruction_pointer = operand
            continue
    elif opcode == 4:
        # bxc
        b = b ^ c
    elif opcode == 5:
        # out
        output.append(str(get_combo_operand_value(operand, a, b, c) % 8))
    elif opcode == 6:
        # bdv
        numerator = a
        denominator = 2 ** get_combo_operand_value(operand, a, b, c)
        b = numerator // denominator
    elif opcode == 7:
        # cdv
        numerator = a
        denominator = 2 ** get_combo_operand_value(operand, a, b, c)
        c = numerator // denominator
    else:
        raise

    instruction_pointer += 2

print(','.join(output))

