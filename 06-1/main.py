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


def get_right_direction(current_direction):
    if current_direction == 'n':
        return 'e'
    elif current_direction == 'e':
        return 's'
    elif current_direction == 's':
        return 'w'
    else:
        return 'n'


def move_next(obstructions, max_x, max_y, current_location, facing):
    next_direction = facing
    next_location = get_next_location(current_location, facing)

    if next_location in obstructions:
        next_direction = get_right_direction(facing)
        next_location = get_next_location(current_location, next_direction)

    next_x = next_location[0]
    next_y = next_location[1]
    if next_x < 0 or next_x > max_x or next_y < 0 or next_y > max_y:
        return (None, next_direction)

    return (next_location, next_direction)


with open(os.path.join(os.path.dirname(__file__), "input.txt")) as f:
    lines = f.readlines()

obstructions = set()
start = (0, 0)
max_x = len(lines[0].strip()) - 1
max_y = -1
for row in range(0, len(lines)):
    line = lines[row].strip()
    if line == '':
        continue

    max_y += 1

    row_data = list(line)
    for col in range(0, len(row_data)):
        if row_data[col] == '#':
            obstructions.add((col, row))
        elif row_data[col] == '^':
            start = (col, row)

locations_visited = {start}
current_location = start
facing = 'n'
while current_location is not None:
    (current_location, facing) = move_next(obstructions, max_x, max_y, current_location, facing)
    if current_location is not None:
        locations_visited.add(current_location)

print(len(locations_visited))
