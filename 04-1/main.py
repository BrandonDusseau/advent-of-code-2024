import os
from pprint import pprint


def get_next_location(origin, direction):
    next_x = origin[0]
    next_y = origin[1]
    if 'n' in direction:
        next_y -= 1
    if 's' in direction:
        next_y += 1
    if 'e' in direction:
        next_x += 1
    if 'w' in direction:
        next_x -= 1

    return (next_x, next_y)


def check_direction(grid, origin, current_letter, direction):
    next_loc = get_next_location(origin, direction)
    (next_x, next_y) = next_loc

    # Don't go out of bounds.
    if next_x < 0 or next_x >= len(grid[0]) or next_y < 0 or next_y >= len(grid):
        return False

    # If the next letter isn't the one that's supposed to come after the current,
    # abandon this path.
    valid_moves = { 'X': 'M', 'M': 'A', 'A': 'S' }
    next_letter = grid[next_x][next_y]
    if valid_moves[current_letter] != next_letter:
        return False

    # If the path so far is valid and we found S, we've found an XMAS.
    if next_letter == 'S':
        return True

    # Recurse to check the next letter.
    return check_direction(grid, next_loc, next_letter, direction)


with open(os.path.join(os.path.dirname(__file__), "input.txt")) as f:
    lines = f.readlines()

# Generate a grid and find all the X's.
grid = []
x_locs = []
cur_row = 0
for line in lines:
    row = list(line.strip())
    grid.append(row)
    x_locs = x_locs + [(cur_row, i) for i, x in enumerate(row) if x == 'X']
    cur_row += 1

# Recursively check each cell around the X to determine if it can spell XMAS.
xmas_found = 0
directions = ['n', 'ne', 'e', 'se', 's', 'sw', 'w', 'nw']
for x_loc in x_locs:
    for direction in directions:
        if check_direction(grid, x_loc, 'X', direction):
            xmas_found += 1

print(xmas_found)

