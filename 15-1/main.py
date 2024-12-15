import os
from pprint import pprint


def get_next_point(origin, direction):
    if direction == '^':
        return (origin[0], origin[1] - 1)
    elif direction == 'v':
        return (origin[0], origin[1] + 1)
    elif direction == '>':
        return (origin[0] + 1, origin[1])
    elif direction == '<':
        return (origin[0] - 1, origin[1])


def move_object(origin, walls, packages, direction):
    next_point = get_next_point(origin, direction)
    if next_point in walls:
        return origin

    if next_point in packages:
        packages.remove(next_point)
        packages.add(move_object(next_point, walls, packages, direction))

    point_to_return = next_point if next_point not in packages else origin

    return point_to_return


with open(os.path.join(os.path.dirname(__file__), "input.txt")) as f:
    lines = f.readlines()

walls = set()
packages = set()
robot = None
moves = []

is_processing_moves = False
read_row = 0
for line in lines:
    stripped_line = line.strip()
    if stripped_line == '':
        is_processing_moves = True
        continue
    if is_processing_moves:
        moves += stripped_line
        continue
    for col in range(0, len(stripped_line)):
        char = stripped_line[col]
        point = (col, read_row)
        if char == '#':
            walls.add(point)
        elif char == 'O':
            packages.add(point)
        elif char == '@':
            robot = point
    read_row += 1

for direction in moves:
    robot = move_object(robot, walls, packages, direction)

coordinate_sum = 0
for package in packages:
    distance_from_left, distance_from_top = package
    coordinate_sum += (100 * distance_from_top) + distance_from_left

print(coordinate_sum)
