import os
from pprint import pprint


def design_is_possible(towels, design, progress, valid_combinations, memo, recursion_level=0):
    print(f"{'  ' * recursion_level}Design {design}")
    start = 0
    end = len(design) - 1

    memo_key = design

    if memo_key in memo:
        print(f"{'  ' * recursion_level}Design is cached")
        return memo[memo_key]

    while start <= end:
        for temp_end in range(end, start - 1, -1):
            print(f"{'  ' * recursion_level}{temp_end}")
            design_subset = design[start:temp_end + 1]
            if design_subset in towels:
                if temp_end + 1 > end:
                    # If the design is valid and we don't have any further design left to check, store this valid design.
                    print(f"{'  ' * recursion_level}{design_subset} is valid and reached end, so storing this combo")
                    valid_combinations.append(progress + [design_subset])
                else:
                    print(f"{'  ' * recursion_level}{design_subset} is valid - recursing with remaining design")
                    if design_is_possible(towels, design[temp_end + 1:end + 1], progress + [design_subset], valid_combinations, memo, recursion_level + 1):
                        print(f"{'  ' * recursion_level}Recursed design {design[temp_end + 1:end + 1]} was valid")
                    else:
                        print(f"{'  ' * recursion_level}Recursed design {design[temp_end + 1:end + 1]} was NOT valid")
            else:
                print(f"{'  ' * recursion_level}Design subset {design_subset} is not a valid towel")

            if temp_end == start:
                # If the remaining design wasn't possible and there's only one stripe left, the design is not possible.
                print(f"{'  ' * recursion_level}Reached the end")
                memo[memo_key] = False
                return False

    memo[memo_key] = True
    return True


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

possible_designs = []
valid_combinations = []
memo = {}
for design in designs:
    if design_is_possible(towels, design, [], valid_combinations, memo):
        possible_designs.append(design)

pprint(valid_combinations)
print(len(valid_combinations))
