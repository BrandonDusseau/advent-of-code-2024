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


def move_object(origin, walls, packages_left, packages_right, direction, is_package):
    # print(f"Moving {'package' if is_package else 'robot'} at ({origin[0]}, {origin[1]}) in direction {direction}")
    is_moving_vertically = direction in {'^', 'v'}
    next_point = get_next_point(origin, direction)
    if next_point in walls:
        # print("  Would be in wall, so not moving")
        return origin

    # If we're a package, check that the right side of the package won't hit a wall.
    right_of_next_point = (next_point[0] + 1, next_point[1])
    if is_package and right_of_next_point in walls:
        # print("  Right side of package would be in wall, so not moving")
        return origin

    packages_to_move = []
    if next_point in packages_left or next_point in packages_right or (is_package and direction == '>' and (next_point[0] + 1, next_point[1]) in packages_left):
        if direction == '<':
            # No matter what we are, if we bump into a package to the left, its left side is two spaces away.
            packages_to_move.append((next_point[0] - 1, next_point[1]))
        elif direction == '>':
            # If we're a robot, the package is directly to our right. If we're a package, it's two spaces to the right.
            packages_to_move.append((next_point[0] + 1, next_point[1]) if is_package else next_point)
        else:
            # The package directly above us or below us. No matter what, we need to move its left side.
            packages_to_move.append((next_point[0] - 1, next_point[1]) if next_point in packages_right else next_point)
        # print(f"  Encountered a package at ({packages_to_move[0][0]}, {packages_to_move[0][1]}), so moving it.")

    # If we're a package and moving vertically, we may also need to move a package thar our right side touches.
    # The is only if our right side is touching the left side of a package. If it's touching the right side, our left
    # side is already handling moving it.
    if is_package and is_moving_vertically and right_of_next_point in packages_left:
        # print(f"  Also encountered another package at ({right_of_next_point[0]}, {right_of_next_point[1]}), so moving that too.")
        packages_to_move.append(right_of_next_point)

    if len(packages_to_move) != 0:
        # Back up the package state.
        packages_left_backup = packages_left.copy()
        packages_right_backup = packages_right.copy()

        all_packages_moved = True
        for package_left_side in packages_to_move:
            package_right_side = (package_left_side[0] + 1, package_left_side[1])
            packages_left.remove(package_left_side)
            packages_right.remove(package_right_side)

            new_package_position = move_object(package_left_side, walls, packages_left, packages_right, direction, True)
            if new_package_position == package_left_side:
                all_packages_moved = False
                break

            packages_left.add(new_package_position)
            packages_right.add((new_package_position[0] + 1, new_package_position[1]))

        # If we couldn't successfully move all the packages, revert to the previous positions.
        if not all_packages_moved:
            # print("  Failed to move at least one package, so undoing movements.")
            packages_left.clear()
            packages_left.update(packages_left_backup)
            packages_right.clear()
            packages_right.update(packages_right_backup)

        # If we moved all the packages, report our new location back. Otherwise report our original location.
        point_to_return = next_point if all_packages_moved else origin
    else:
        point_to_return = next_point

    # print(f"  Next point is ({point_to_return[0]}, {point_to_return[1]})")
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

# visualize(robot, walls, packages_left, packages_right, max_row, max_col)
for direction in moves:
    # print(direction)
    robot = move_object(robot, walls, packages_left, packages_right, direction, False)
    # visualize(robot, walls, packages_left, packages_right, max_row, max_col)

coordinate_sum = 0
for package in packages_left:
    distance_from_left, distance_from_top = package
    coordinate_sum += (100 * distance_from_top) + distance_from_left

print(coordinate_sum)
