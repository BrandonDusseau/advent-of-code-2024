import os
from pprint import pprint


def is_point_in_region(plant, plots, row, col, max_row, max_col):
    if row < 0 or col < 0 or row > max_row or col > max_col:
        return False
    return plots[row][col] == plant


def get_next_point(direction, row, col, max_row, max_col):
    if direction == 's':
        point = (col, row + 1)
    elif direction == 'n':
        point = (col, row - 1)
    elif direction == 'e':
        point = (col + 1, row)
    else:
        point = (col - 1, row)

    if point[1] < 0 or point[0] < 0 or point[1] > max_row or point[0] > max_col:
        return None

    return point


def get_next_direction(direction):
    if direction == 's':
        return 'e'
    elif direction == 'e':
        return 'n'
    elif direction == 'n':
        return 'w'
    else:
        return 's'


def explore_region(discovered, plots, row, col, max_row, max_col):
    if (col, row) in discovered:
        return set()

    discovered.add((col, row))
    adjacent_plots_in_region = []
    plant = plots[row][col]

    points_to_test = [
        (col - 1, row),
        (col + 1, row),
        (col, row - 1),
        (col, row + 1)
    ]
    for test_col, test_row in points_to_test:
        if is_point_in_region(plant, plots, test_row, test_col, max_row, max_col):
            adjacent_plots_in_region.append((test_col, test_row))

    plots_in_region = {(col, row)}
    for plot_col, plot_row in adjacent_plots_in_region:
        found_plots = explore_region(discovered, plots, plot_row, plot_col, max_row, max_col)
        plots_in_region = plots_in_region.union(found_plots)

    return plots_in_region


with open(os.path.join(os.path.dirname(__file__), "input.txt")) as f:
    lines = f.readlines()

plots = []
for line in lines:
    stripped_line = line.strip()
    if stripped_line == '':
        continue
    plots.append(stripped_line)

max_row = len(plots) - 1
max_col = len(plots[0]) - 1

points_assigned_regions = set()
regions = {}
for row in range(0, len(plots)):
    for col in range(0, len(plots[row])):
        if (col, row) in points_assigned_regions:
            continue
        region = explore_region(set(), plots, row, col, max_row, max_col)
        regions[(col, row)] = region
        points_assigned_regions = points_assigned_regions.union(region)

total_price = 0
for top_left_point, region_points in regions.items():
    sides = 1
    direction = 's'
    current_point = top_left_point
    initial_point = True
    while initial_point or current_point != top_left_point:
        pprint(current_point)
        initial_point = False
        next_point = get_next_point(direction, current_point[1], current_point[0], max_row, max_col)
        while next_point not in region_points:
            sides += 1
            direction = get_next_direction(direction)
            next_point = get_next_point(direction, current_point[1], current_point[0], max_row, max_col)
        current_point = next_point
    print(sides)
    print()
    total_price += len(region_points) * sides

print(total_price)
