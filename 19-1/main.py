import os
from pprint import pprint


def design_is_possible(towels, design, recursion_level=0):
    print(f"{'  ' * recursion_level}Design {design}")
    start = 0
    end = len(design) - 1

    while start <= end:
        for temp_end in range(end, start - 1, -1):
            if design[start:temp_end + 1] in towels:
                print(f"{'  ' * recursion_level}{design[start:temp_end + 1]} is valid - recursing with remaining design")
                if temp_end + 1 > end:
                    # If the design is valid and we don't have any further design left to check, return true.
                    return True
                elif design_is_possible(towels, design[temp_end + 1:end + 1], recursion_level + 1):
                    # If the remaining design is possible, return true.
                    return True
                elif temp_end == start:
                    print(f"{'  ' * recursion_level}Recursion failed, and we're out of stripes - not possible to continue")
                    return False
            elif temp_end == start:
                # If the remaining design wasn't possible and there's only one stripe left, the design is not possible.
                print(f"{'  ' * recursion_level}{design[start]} is NOT valid - Not possible to continue")
                return False
            else:
                print(f"{'  ' * recursion_level}{design[start:temp_end + 1]} is NOT valid")

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
for design in designs:
    if design_is_possible(towels, design):
        possible_designs.append(design)

pprint(possible_designs)
print(len(possible_designs))
