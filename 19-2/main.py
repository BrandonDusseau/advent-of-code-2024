import os
from pprint import pprint


def get_possible_combinations(design, towels, memo, recursion_depth=0):
    if design in memo:
        # print(f"{' ' * recursion_depth}Design {design} is cached - returning results.")
        return memo[design]

    if design == '':
        # print(f"{' ' * recursion_depth}Got blank design, going back up.")
        return 0

    if len(design) == 1:
        if design in towels:
            # print(f"{' ' * recursion_depth}Remaining design is a valid towellllll, so returning it.")
            memo[design] = 1
            return 1
        else:
            # print(f"{' ' * recursion_depth}Remaining design is not a valid towel - returning none.")
            memo[design] = 0
            return 0

    viable_combinations = 0
    segment_length = 1
    while segment_length <= len(design):
        segment = design[0:segment_length]
        remainder = design[segment_length:]
        if segment not in towels:
            # print(f"{' ' * recursion_depth}Prefix {segment} is not valid. Continuing.")
            segment_length += 1
            continue
        # print(f"{' ' * recursion_depth}Starting with valid prefix {segment} - recursing with {remainder}")
        if remainder == '':
            # print(f"{' ' * recursion_depth}No remaining design, so adding {segment} to results.")
            viable_combinations += 1
            segment_length += 1
            continue
        viable_combinations += get_possible_combinations(remainder, towels, memo, recursion_depth + 1)

        segment_length += 1
    memo[design] = viable_combinations
    return viable_combinations


with open(os.path.join(os.path.dirname(__file__), "input.txt")) as f:
    lines = f.readlines()

towels = set()
designs = []
reading_designs = False
for line in lines:
    stripped_line = line.strip()
    if stripped_line == '':
        reading_designs = True
        continue

    if reading_designs:
        designs.append(stripped_line)
    else:
        towels = set(stripped_line.split(', '))

valid_combinations = 0
memo = {}
design_index = 0
for design in designs:
    print(f"Processing design {design} with index {design_index}")
    valid_combinations += get_possible_combinations(design, towels, memo)
    design_index += 1

print(valid_combinations)
