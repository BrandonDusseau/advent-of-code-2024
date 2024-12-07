import os
from pprint import pprint


def visualize(potential_obstruction, lines, max_x, max_y, visited_locations):
    for row in range(0, max_y + 1):
        row_chars = []
        for col in range(0, max_x + 1):
            char = lines[row][col]
            if char == '.':
                if potential_obstruction == (col, row):
                    row_chars.append('O')
                    continue
                for loc in visited_locations:
                    (location, direction) = loc
                    if location == (col, row):
                        if (direction == 'n' or direction == 's') and char == '-':
                            char = '+'
                        elif (direction == 'n' or direction == 's') and char == '.':
                            char = '|'
                        elif (direction == 'e' or direction == 'w') and char == '|':
                            char = '+'
                        elif (direction == 'e' or direction == 'w') and char == '.':
                            char = '-'
            row_chars.append(char)
        print(''.join(row_chars))
    print()


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


def move_next(obstructions, max_x, max_y, current_location, current_direction):
    next_direction = current_direction
    next_location = get_next_location(current_location, current_direction)
    encountered_obstruction = None

    while next_location in obstructions:
        encountered_obstruction = next_location
        next_direction = get_right_direction(next_direction)
        next_location = get_next_location(current_location, next_direction)

    next_x = next_location[0]
    next_y = next_location[1]
    if next_x < 0 or next_x > max_x or next_y < 0 or next_y > max_y:
        return (None, next_direction, encountered_obstruction)

    return (next_location, next_direction, encountered_obstruction)


def simulate_obstruction(start_location, start_direction, locations_visited, obstructions, max_x, max_y, potential_obstruction, lines, should_visualize):
    #print(f"Placing obstruction at ({potential_obstruction[0]}, {potential_obstruction[1]})")
    mock_obstructions = obstructions.copy()
    mock_obstructions.add(potential_obstruction)
    next_location = start_location
    next_direction = start_direction

    # Continue until the guard either encounters a position + direction they've already been in or until they exit.
    seen_locations = set(locations_visited)
    seen_locations.add((start_location, start_direction))
    while next_location is not None:
        prev_location = next_location
        (next_location, next_direction, encountered_obstruction) = move_next(mock_obstructions, max_x, max_y, next_location, next_direction)
        loc_info = (next_location, next_direction)

        # We technially moved in two directions if we hit an obstruction, so add the new direction as well.
        if encountered_obstruction is not None:
            seen_locations.add((prev_location, next_direction))

        if loc_info in seen_locations:
            #print("Found cycle!")
            #print()
            if should_visualize:
                visualize(potential_obstruction, lines, max_x, max_y, seen_locations)
            return True

        if next_location is not None:
            #print(f"Moving to ({next_location[0]}, {next_location[1]}) with direction {next_direction}")
            seen_locations.add(loc_info)

    return False


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
current_location = start
facing = 'n'
loop_obstructions = set()
while current_location is not None:
    (prev_location, prev_facing) = locations_visited[-1]
    (current_location, facing, encountered_obstruction) = move_next(obstructions, max_x, max_y, current_location, facing)
    # We technially moved in two directions if we hit an obstruction, so add the new direction as well.
    if encountered_obstruction is not None:
        locations_visited.append((prev_location, facing))

    if current_location is not None:
        locations_visited.append((current_location, facing))

    # Pretend there is an obstruction here and move starting from where we were before.
    if encountered_obstruction is None and current_location != start and current_location is not None:
        #print(f"Starting simulation at ({current_location[0]}, {current_location[1]}) with direction {facing}")
        if simulate_obstruction(start, 'n', [], obstructions, max_x, max_y, current_location, lines, False):
            loop_obstructions.add(current_location)

        # Also run a simulation where the obstruction is placed after the guard moves away.
        # (next_simulated_location, next_simulated_direction, encountered_obstruction_2) = move_next(obstructions, max_x, max_y, current_location, facing)
        # if encountered_obstruction_2 is None and next_simulated_direction != start and next_simulated_location is not None:
        #     if simulate_obstruction(next_simulated_location, next_simulated_direction, locations_visited, obstructions, max_x, max_y, current_location, lines, False):
        #         loop_obstructions.add(current_location)

#pprint(loop_obstructions)
print(len(loop_obstructions))


