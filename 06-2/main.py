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
    encountered_obstruction = None

    if next_location in obstructions:
        encountered_obstruction = next_location
        next_direction = get_right_direction(facing)
        next_location = get_next_location(current_location, next_direction,)

    next_x = next_location[0]
    next_y = next_location[1]
    if next_x < 0 or next_x > max_x or next_y < 0 or next_y > max_y:
        return (None, next_direction, encountered_obstruction)

    return (next_location, next_direction, encountered_obstruction)


def has_seen_obstruction_on_path(found_obstructions, current_location, direction_if_obstruction_placed):
    nearest_obstruction = None
    for (potential_obstruction, obs_encounter_direction) in found_obstructions:
        if obs_encounter_direction != direction_if_obstruction_placed:
            continue
        if direction_if_obstruction_placed == 'n':
            if potential_obstruction[1] > current_location[1] or potential_obstruction[0] != current_location[0]:
                continue
            if nearest_obstruction is None or nearest_obstruction[1] < potential_obstruction[1]:
                nearest_obstruction = potential_obstruction
        elif direction_if_obstruction_placed == 'e':
            if potential_obstruction[0] < current_location[0] or potential_obstruction[1] != current_location[1]:
                continue
            elif nearest_obstruction is None or nearest_obstruction[0] > potential_obstruction[0]:
                nearest_obstruction = potential_obstruction
        elif direction_if_obstruction_placed == 's':
            if potential_obstruction[1] < current_location[1] or potential_obstruction[0] != current_location[0]:
                continue
            elif nearest_obstruction is None or nearest_obstruction[1] > potential_obstruction[1]:
                nearest_obstruction = potential_obstruction
        else:
            if potential_obstruction[0] > current_location[0] or potential_obstruction[1] != current_location[1]:
                continue
            elif nearest_obstruction is None or nearest_obstruction[0] < potential_obstruction[0]:
                nearest_obstruction = potential_obstruction

    if nearest_obstruction is None:
        print(f"    There is no obstruction along that path.")
    else:
        print(f"    Nearest obstruction at {nearest_obstruction[0]}, {nearest_obstruction[1]}")
    return nearest_obstruction is not None


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

locations_visited = [(start, 'n')] # (Location, direction after moving)
found_obstructions = [] # (location, direction when encountered)
current_location = start
facing = 'n'
potential_obstructions = set()
while current_location is not None:
    prev_facing = facing
    (current_location, facing, encountered_obstruction) = move_next(obstructions, max_x, max_y, current_location, facing)
    if current_location is not None:
        locations_visited.append((current_location, facing))

    # Record where the obstructions were found and what direction they were hit from.
    if encountered_obstruction is not None:
        found_obstructions.append(((encountered_obstruction), prev_facing))

# Find all the places where adding an obstruction would cause the guard to run into another obstruction.
for i in range(1, len(locations_visited)):
    (prev_location, prev_direction) = locations_visited[i - 1]
    (current_location, current_direction) = locations_visited[i]
    direction_if_obstruction_placed = get_right_direction(prev_direction)
    print(f"Now at {current_location[0]}, {current_location[1]} facing the {current_direction} direction")
    print(f"  If there were an obstruction here, If we did we would turn {direction_if_obstruction_placed} at {prev_location[0]}, {prev_location[1]}")
    if has_seen_obstruction_on_path(found_obstructions, prev_location, direction_if_obstruction_placed):
            potential_obstructions.add(current_location)

# Of those obstructions, narrow them down to ones that cause a cycle.
loop_obstructions = set()
for potential_obstruction in potential_obstructions:
    mock_obstructions = set(list(obstructions) + [potential_obstruction])
    locations_visited = {(start, 'n')}
    facing = 'n'
    current_location = start
    while current_location is not None:
        prev_facing = facing
        (current_location, facing, encountered_obstruction) = move_next(mock_obstructions, max_x, max_y, current_location, facing)
        if (current_location, facing) in locations_visited:
            loop_obstructions.add(potential_obstruction)
            break
        if current_location is not None:
            locations_visited.add((current_location, facing))


pprint(loop_obstructions)
print(len(loop_obstructions))


