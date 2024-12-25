import os
from collections import defaultdict
from pprint import pprint


def is_point_in_region(plant, plots, row, col, max_row, max_col):
    if row < 0 or col < 0 or row > max_row or col > max_col:
        return False
    return plots[row][col] == plant


def explore_region(discovered, plots, row, col, max_row, max_col):
    if (col, row) in discovered:
        return (set(), {})

    discovered.add((col, row))
    adjacent_plots_in_region = []
    walls = defaultdict(list)
    plant = plots[row][col]

    points_to_test = [
        ((col - 1, row), 'e'),
        ((col + 1, row), 'w'),
        ((col, row - 1), 'n'),
        ((col, row + 1), 's')
    ]
    for test_point, direction in points_to_test:
        test_col, test_row = test_point
        if is_point_in_region(plant, plots, test_row, test_col, max_row, max_col):
            adjacent_plots_in_region.append((test_col, test_row))
        else:
            walls[direction].append((test_col, test_row))

    plots_in_region = {(col, row)}
    for plot_col, plot_row in adjacent_plots_in_region:
        (found_plots, found_walls) = explore_region(discovered, plots, plot_row, plot_col, max_row, max_col)
        plots_in_region = plots_in_region.union(found_plots)
        for wall_direction, wall_points in found_walls.items():
            walls[wall_direction] += wall_points

    return (plots_in_region, walls)


def count_gaps(wall_dict):
    sides = 0
    for _, values in wall_dict.items():
        sorted_values = sorted(values)
        for i in range(1, len(sorted_values)):
            if abs(sorted_values[i] - sorted_values[i - 1]) > 1:
                sides += 1
    return sides


def count_sides(walls):
    north_walls_by_row = defaultdict(list)
    for wall in walls['n']:
        north_walls_by_row[wall[1]].append(wall[0])
    south_walls_by_row = defaultdict(list)
    for wall in walls['s']:
        south_walls_by_row[wall[1]].append(wall[0])
    east_walls_by_col = defaultdict(list)
    for wall in walls['e']:
        east_walls_by_col[wall[0]].append(wall[1])
    west_walls_by_col = defaultdict(list)
    for wall in walls['w']:
        west_walls_by_col[wall[0]].append(wall[1])

    # The base number of sides is how many different rows (n/s) or cols (e/w) are represented.
    sides = len(north_walls_by_row) + len(south_walls_by_row) + len(east_walls_by_col) + len(west_walls_by_col)

    # Gaps in the given rows/cols add additional sides.
    sides += count_gaps(north_walls_by_row)
    sides += count_gaps(south_walls_by_row)
    sides += count_gaps(east_walls_by_col)
    sides += count_gaps(west_walls_by_col)

    return sides


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
regions = []
for row in range(0, len(plots)):
    for col in range(0, len(plots[row])):
        if (col, row) in points_assigned_regions:
            continue
        region = explore_region(set(), plots, row, col, max_row, max_col)
        regions.append(region)
        points_assigned_regions = points_assigned_regions.union(region[0])

total_price = 0
for region_data in regions:
    region_points, region_walls = region_data
    pprint(region_points)
    total_sides = count_sides(region_walls)
    print(total_sides)
    print()
    total_price += len(region_points) * total_sides

print(total_price)
