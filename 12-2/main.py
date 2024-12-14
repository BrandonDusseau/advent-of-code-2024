import os
from pprint import pprint


def is_point_in_region(plant, plots, row, col, max_row, max_col):
    if row < 0 or col < 0 or row > max_row or col > max_col:
        return False
    return plots[row][col] == plant


def explore_region(discovered, plots, row, col, max_row, max_col):
    if (col, row) in discovered:
        return (set(), set())

    discovered.add((col, row))
    adjacent_plots_in_region = []
    walls = []
    plant = plots[row][col]

    points_to_test = [
        ((col - 1, row), 'vert'),
        ((col + 1, row), 'vert'),
        ((col, row - 1), 'horiz'),
        ((col, row + 1), 'horiz')
    ]
    for test_point, direction in points_to_test:
        test_col, test_row = test_point
        if is_point_in_region(plant, plots, test_row, test_col, max_row, max_col):
            adjacent_plots_in_region.append((test_col, test_row))
        else:
            walls.append(((test_col, test_row), direction))

    plots_in_region = {(col, row)}
    for plot_col, plot_row in adjacent_plots_in_region:
        (found_plots, found_walls) = explore_region(discovered, plots, plot_row, plot_col, max_row, max_col)
        plots_in_region = plots_in_region.union(found_plots)
        walls += found_walls

    return (plots_in_region, walls)


def count_sides(walls):
    vert_corners = []
    horiz_corners = []
    wall_lookup = set(walls)

    for current_point, direction in walls:
        col, row = current_point

        print(f"Processing point ({col}, {row}) - {direction} wall")

        points_to_test = [
            (col - 1, row),
            (col + 1, row)
        ]

        if direction == 'vert':
            points_to_test = [
                (col, row - 1),
                (col, row + 1)
            ]

        if (points_to_test[0], direction) not in wall_lookup:
            print(f"  Adding point ({points_to_test[0][0]}, {points_to_test[0][1]})")
            if direction == 'vert':
                vert_corners.append(points_to_test[0])
            else:
                horiz_corners.append(points_to_test[0])

        if (points_to_test[1], direction) not in wall_lookup:
            print(f"  Adding point ({points_to_test[1][0]}, {points_to_test[1][1]})")
            if direction == 'vert':
                vert_corners.append(points_to_test[1])
            else:
                horiz_corners.append(points_to_test[1])

    return max(len(vert_corners), len(horiz_corners))


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

pprint(regions)

total_price = 0
for region_data in regions:
    region_points, region_walls = region_data
    pprint(region_points)
    total_sides = count_sides(region_walls)
    print(total_sides)
    print()
    total_price += len(region_points) * total_sides

print(total_price)
