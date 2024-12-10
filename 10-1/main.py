import os
from pprint import pprint


def get_possible_directions(current_location, seen_locations, max_row, max_col):
    directions = []
    (current_col, current_row) = current_location
    if current_col != 0:
        directions.append((current_col - 1, current_row))
    if current_col != max_col:
        directions.append((current_col + 1, current_row))
    if current_row != 0:
        directions.append((current_col, current_row - 1))
    if current_row != max_row:
        directions.append((current_col, current_row + 1))

    return [direction for direction in directions if direction not in seen_locations]


def explore_trail(current_location, expected_number, seen_locations, map, max_row, max_col):
    (current_col, current_row) = current_location

    if (map[current_row][current_col] != expected_number):
        return []

    if (expected_number == 9):
        return [current_location]

    reachable_peaks = []
    next_seen_locations = seen_locations.copy()
    next_seen_locations.append(current_location)
    for next_hop in get_possible_directions(current_location, seen_locations, max_row, max_col):
        reachable_peaks += explore_trail(next_hop, expected_number + 1, next_seen_locations, map, max_row, max_col)

    return reachable_peaks


with open(os.path.join(os.path.dirname(__file__), "input.txt")) as f:
    lines = f.readlines()

trailheads = []
map = []
max_row = -1
max_col = 0
for row in range(0, len(lines)):
    this_row = []
    max_row += 1
    line = lines[row].strip()
    max_col = len(line) - 1
    for col in range(0, len(line)):
        this_row.append(int(line[col]))
        if line[col] == '0':
            trailheads.append((col, row))
    map.append(this_row)

scores = []
for trailhead in trailheads:
    result = set(explore_trail(trailhead, 0, [], map, max_row, max_col))
    if len(result) == 0:
        continue
    scores.append(len(result))

print(sum(scores))
