import os
from pprint import pprint


def visualize(robot, walls, packages_left, packages_right, max_row, max_col):
    for row in range(0, max_row + 1):
        row_data = []
        for col in range(0, (max_col * 2) + 2):
            char = '.'
            point = (col, row)
            if point in walls:
                char = '#'
            elif point in packages_left:
                char = '['
            elif point in packages_right:
                char = ']'
            elif point == robot:
                char = '@'
            row_data.append(char)
        print(''.join(row_data))


def get_next_point(origin, direction):
    if direction == '^':
        return (origin[0], origin[1] - 1)
    elif direction == 'v':
        return (origin[0], origin[1] + 1)
    elif direction == '>':
        return (origin[0] + 1, origin[1])
    elif direction == '<':
        return (origin[0] - 1, origin[1])


def move_object(origin, walls, packages_left, packages_right, direction):
    # print(f"Moving object at ({origin[0]}, {origin[1]}) in direction {direction}")
    next_point = get_next_point(origin, direction)
    if next_point in walls:
        # print("  Found wall, so not moving")
        return origin

    if next_point in packages_left or next_point in packages_right:
        # print("  Encountered a package, so moving the package")
        package_left_original = next_point if next_point in packages_left else (next_point[0] - 1, next_point[1])
        package_right_original = next_point if next_point in packages_right else (next_point[0] + 1, next_point[1])

        packages_left.remove(package_left_original)
        packages_right.remove(package_right_original)

        package_left_new = move_object(package_left_original, walls, packages_left, packages_right, direction)
        package_right_new = move_object(package_right_original, walls, packages_left, packages_right, direction)

        package_moved = package_left_new != package_left_original and package_right_new != package_right_original

        if package_moved:
            packages_left.add(package_left_new)
            packages_right.add(package_right_new)
        else:
            packages_left.add(package_left_original)
            packages_right.add(package_right_original)

    point_to_return = next_point if next_point not in packages_left and next_point not in packages_right else origin

    # print(f"  Moved to ({point_to_return[0]}, {point_to_return[1]})")
    return point_to_return


with open(os.path.join(os.path.dirname(__file__), "input.txt")) as f:
    lines = f.readlines()

walls = set()
packages_left = set()
packages_right = set()
robot = None
moves = []

is_processing_moves = False
read_row = 0
max_col = 0
for line in lines:
    stripped_line = line.strip()
    if stripped_line == '':
        is_processing_moves = True
        continue
    if is_processing_moves:
        moves += stripped_line
        continue
    max_col = len(stripped_line) - 1
    for col in range(0, len(stripped_line)):
        char = stripped_line[col]
        point = (col * 2, read_row)
        if char == '#':
            walls.add(point)
            walls.add(((col * 2) + 1, read_row))
        elif char == 'O':
            packages_left.add(point)
            packages_right.add(((col * 2) + 1, read_row))
        elif char == '@':
            robot = point
    read_row += 1
max_row = read_row - 1

visualize(robot, walls, packages_left, packages_right, max_row, max_col)
for direction in moves:
    print(direction)
    robot = move_object(robot, walls, packages_left, packages_right, direction)
    visualize(robot, walls, packages_left, packages_right, max_row, max_col)

coordinate_sum = 0
for package in packages_left:
    distance_from_left, distance_from_top = package
    coordinate_sum += (100 * distance_from_top) + distance_from_left

print(coordinate_sum)
