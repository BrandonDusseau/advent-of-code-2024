import os
from pprint import pprint


def is_point_in_region(plant, plots, row, col, max_row, max_col):
    if row < 0 or col < 0 or row > max_row or col > max_col:
        return False
    return plots[row][col] == plant


def explore_region(discovered, plots, row, col, max_row, max_col):
    if (col, row) in discovered:
        return (set(), 0)

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

    total_sides = 4 - len(adjacent_plots_in_region)
    plots_in_region = {(col, row)}
    for plot_col, plot_row in adjacent_plots_in_region:
        (found_plots, sides) = explore_region(discovered, plots, plot_row, plot_col, max_row, max_col)
        total_sides += sides
        plots_in_region = plots_in_region.union(found_plots)

    return (plots_in_region, total_sides)


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
        region_points, region_sides = explore_region(set(), plots, row, col, max_row, max_col)
        region = (region_points, region_sides, plots[row][col])
        regions.append(region)
        points_assigned_regions = points_assigned_regions.union(region[0])

total_price = 0
for region in regions:
    total_price += len(region[0]) * region[1]

print(total_price)
