import os
from pprint import pprint


def check_mases(grid, origin):
    origin_x = origin[0]
    origin_y = origin[1]

    # Don't go out of bounds.
    if origin_x < 1 or origin_x >= len(grid[0]) - 1 or origin_y < 1 or origin_y >= len(grid) - 1:
        return False

    forward_diag = set()  # /
    backward_diag = set() # \

    # Get all the letters in an X shape around the origin.
    forward_diag.add(grid[origin_x + 1][origin_y - 1])
    forward_diag.add(grid[origin_x - 1][origin_y + 1])
    backward_diag.add(grid[origin_x - 1][origin_y - 1])
    backward_diag.add(grid[origin_x + 1][origin_y + 1])

    # The X is valid if each slant has exactly one M and exactly one S.
    forward_diag_valid = 'M' in forward_diag and 'S' in forward_diag
    backward_diag_valid = 'M' in backward_diag and 'S' in backward_diag
    return forward_diag_valid and backward_diag_valid


with open(os.path.join(os.path.dirname(__file__), "input.txt")) as f:
    lines = f.readlines()

# Generate a grid and find all the A's.
grid = []
a_locs = []
cur_row = 0
for line in lines:
    row = list(line.strip())
    grid.append(row)
    a_locs = a_locs + [(cur_row, i) for i, x in enumerate(row) if x == 'A']
    cur_row += 1

# Check the four corners of each A to determine if the MASes are valid.
mas_found = 0
for a_loc in a_locs:
    if check_mases(grid, a_loc):
        mas_found += 1

print(mas_found)
