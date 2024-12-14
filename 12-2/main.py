import os
from pprint import pprint


def is_point_in_region(plant, plots, row, col, max_row, max_col):
    if row < 0 or col < 0 or row > max_row or col > max_col:
        return False
    return plots[row][col] == plant


def explore_region(discovered, plots, row, col, max_row, max_col):
    if (col, row) in discovered:
        return (set(), [])

    discovered.add((col, row))
    adjacent_plots_in_region = []
    walls = []
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
        else:
            walls.append((test_col, test_row))

    plots_in_region = {(col, row)}
    for plot_col, plot_row in adjacent_plots_in_region:
        (found_plots, found_walls) = explore_region(discovered, plots, plot_row, plot_col, max_row, max_col)
        plots_in_region = plots_in_region.union(found_plots)
        walls += found_walls

    return (plots_in_region, sorted(walls))


def count_sides(walls, top_left_point):
    sides = 0
    processed_walls = set()
    walls_to_process = walls.copy()
    pprint(walls)

    current_point = (top_left_point[0], top_left_point[1] - 1)
    while current_point is not None:
        col, row = current_point
        print(f"Processing point ({col}, {row})")
        processed_walls.add(current_point)
        walls_to_process.remove(current_point)

        points_to_test = [
            (col - 1, row),
            (col + 1, row),
            (col, row - 1),
            (col, row + 1)
        ]

        # Try moving to an adjacent wall.
        next_point = None
        for test_point in points_to_test:
            if test_point in walls and test_point not in processed_walls:
                print(f"  Found adjacent point at ({test_point[0]}, {test_point[1]})")
                next_point = test_point
                break

        # If there are no adjacent points, pick the next wall that isn't already processed.
        if next_point is None:
            sides += 1
            print(f"  Starting another wall.")
            next_point = next(iter(walls_to_process)) if len(walls_to_process) > 0 else None

        current_point = next_point

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
regions = {}
for row in range(0, len(plots)):
    for col in range(0, len(plots[row])):
        if (col, row) in points_assigned_regions:
            continue
        region = explore_region(set(), plots, row, col, max_row, max_col)
        regions[(col, row)] = region
        points_assigned_regions = points_assigned_regions.union(region[0])

total_price = 0
for top_left_point, region_data in regions.items():
    region_points, region_walls = region_data
    pprint(region_points)
    total_sides = count_sides(region_walls, top_left_point)
    print(total_sides)
    print()
    total_price += len(region_points) * total_sides

print(total_price)
