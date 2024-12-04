import os
from pprint import pprint

with open(os.path.join(os.path.dirname(__file__), "input.txt")) as f:
    lines = f.readlines()

grid = []
x_locs = []

# Generate a grid and find all the X's.
cur_row = 0
for line in lines:
    row = list(line.strip())
    grid.append(row)
    x_locs = x_locs + [(cur_row, i) for i, x in enumerate(row) if x == 'X']
    cur_row += 1

pprint(grid)
pprint(x_locs)

