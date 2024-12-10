import hashlib
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

    paths = []
    next_seen_locations = seen_locations.copy()
    next_seen_locations.append(current_location)

    if (expected_number == 9):
        return [next_seen_locations]

    for next_hop in get_possible_directions(current_location, seen_locations, max_row, max_col):
        results = explore_trail(next_hop, expected_number + 1, next_seen_locations, map, max_row, max_col)
        for result_path in results:
            if len(result_path) != 0:
                paths.append(result_path)

    return paths


def get_path_checksum(path):
    path_string = ','.join([f'({x[0]}|{x[1]})' for x in path])
    return hashlib.md5(path_string.encode('utf-8')).hexdigest()


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

ratings = []
for trailhead in trailheads:
    unique_path_sums = set()
    found_paths = explore_trail(trailhead, 0, [], map, max_row, max_col)

    for path in found_paths:
        unique_path_sums.add(get_path_checksum(path))

    if len(unique_path_sums) == 0:
        continue
    ratings.append(len(unique_path_sums))

print(sum(ratings))
