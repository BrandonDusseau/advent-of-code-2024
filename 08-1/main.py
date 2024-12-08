import os
from pprint import pprint


def is_location_valid(max_col, max_row, location):
    (col, row) = location
    return col >= 0 and col <= max_col and row >= 0 and row <= max_row


with open(os.path.join(os.path.dirname(__file__), "input.txt")) as f:
    lines = f.readlines()

antennae = {}
max_row = len(lines) - 1
max_col = len(lines[0].strip()) - 1
for row in range(0, len(lines)):
    line = lines[row].strip()
    for col in range(0, len(line)):
        char = line[col]
        if char != '.':
            if char not in antennae:
                antennae[char] = [(col, row)]
            else:
                antennae[char].append((col, row))

antinodes = set()
for frequency, locations in antennae.items():
    for this_location in locations:
        (this_location_col, this_location_row) = this_location
        for other_location in locations:
            if this_location == other_location:
                continue
            (other_location_col, other_location_row) = other_location
            col_diff = other_location_col - this_location_col
            row_diff = other_location_row - this_location_row
            antinode_location = (this_location_col + (col_diff * 2), this_location_row + (row_diff * 2))
            if is_location_valid(max_col, max_row, antinode_location):
                antinodes.add(antinode_location)

pprint(antinodes)
print(len(antinodes))

