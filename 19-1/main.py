import os
from pprint import pprint


def design_is_possible(towels, design):
    print(f"Design {design}")
    start = 0
    end = len(design) - 1

    backtrack_points = []
    subsets = []
    while start <= end:
        pprint(backtrack_points)
        pprint(subsets)
        for temp_end in range(end, start - 1, -1):
            if design[start:temp_end + 1] in towels:
                print(f"  {design[start:temp_end + 1]} is valid")
                backtrack_points.append(temp_end)
                subsets.append(design[start:temp_end + 1])
                start = temp_end + 1
                break
            elif temp_end == start:
                print("  Not possible to continue")
                return False
            print(f"  {design[start:temp_end + 1]} is NOT valid")

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
