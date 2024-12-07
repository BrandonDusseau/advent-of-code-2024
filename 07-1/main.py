import os
import re
from pprint import pprint


def do_math(operands, running_result, needed_result):
    if len(operands) == 0:
        return running_result if running_result == needed_result else 0

    next_operands = operands.copy()
    this_operand = next_operands.pop(0)

    add_result = running_result + this_operand
    mult_result = running_result * this_operand

    add_total = do_math(next_operands, add_result, needed_result)
    mult_total = do_math(next_operands, mult_result, needed_result)

    return add_total + mult_total


with open(os.path.join(os.path.dirname(__file__), "input.txt")) as f:
    lines = f.readlines()

values = []
for line in lines:
    match = re.findall(r"(\d+)", line.strip())
    values.append((int(match[0]), [int(x) for x in match[1:]]))

total = 0
for (expected_result, operands) in values:
    result = do_math(operands[1:], operands[0], expected_result)
    if result > 0:
        total += expected_result

print(total)
