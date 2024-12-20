import math
import os
from pprint import pprint


def visualize(spaces, walls, start, end, max_x, max_y):
    for y in range(0, max_y + 1):
        row = []
        for x in range(0, max_x + 1):
            point = (x, y)
            if point == start:
                row.append('S')
            elif point == end:
                row.append('E')
            elif point in spaces:
                row.append('.')
            elif point in walls:
                row.append('#')
            else:
                row.append('?')
        print(''.join(row))


def is_point_valid(point, max_x, max_y):
    x, y = point
    return x >= 0 and y >= 0 and x <= max_x and y <= max_y


def get_surrounding_points(point):
    x, y = point
    return [
        (x - 1, y),
        (x + 1, y),
        (x, y - 1),
        (x, y + 1)
    ]


def get_valid_neighbors(point, spaces):
    return [x for x in get_surrounding_points(point) if x in spaces]


def dijkstra(spaces, start):
    dist = {}
    prev = {}
    q = set()
    for point in spaces:
        dist[point] = math.inf
        prev[point] = None
        q.add(point)
    dist[start] = 0

    while len(q) != 0:
        u = None
        min_dist = math.inf
        for v in q:
            if dist[v] <= min_dist:
                u = v
                min_dist = dist[v]

        q.remove(u)

        neighbors = get_valid_neighbors(u, spaces)
        for v in neighbors:
            if v not in q:
                continue

            alt = dist[u] + 1
            if alt < dist[v]:
                dist[v] = alt
                prev[v] = u

    return dist, prev


with open(os.path.join(os.path.dirname(__file__), "input.txt")) as f:
    lines = f.readlines()

walls = set()
spaces = set()
start = None
end = None
max_y = -1
max_x = 0
for line_index in range(0, len(lines)):
    line = lines[line_index].strip()

    if line == '':
        continue

    max_y += 1
    max_x = len(line) - 1
    for x in range(0, len(line)):
        point = (x, max_y)
        char = line[x]
        if char == 'S':
            start = point
        if char == 'E':
            end = point
        if char == '#':
            walls.add(point)
        if char in {'S', 'E', '.'}:
            spaces.add(point)

# visualize(spaces, walls, start, end, max_x, max_y)

dist_from_start, prev_data = dijkstra(spaces, start)
base_time = dist_from_start[end]
print(f"Base time: {base_time} pS")

original_path = []
original_path_set = set()
u = end
if u in prev_data or u == start:
    while u is not None:
        original_path.insert(0, u)
        original_path_set.add(u)
        u = prev_data[u]

# Determine the distance from the end to every other node
dist_from_end, _ = dijkstra(spaces, end)

saved_times = {}
points_traversed = set()
for point1 in original_path:
    points_traversed.add(point1)

    time_from_start = dist_from_start[point1]

    for point2 in spaces:
        cheat_length = abs(point1[0] - point2[0]) + abs(point1[1] - point2[1])
        if cheat_length > 20:
            continue

        time_from_end = dist_from_end[point2]

        # Add the length of the cheat.
        total_time = time_from_start + cheat_length + time_from_end

        diff = base_time - total_time

        if diff <= 0:
            continue

        if diff not in saved_times:
            saved_times[diff] = 1
        else:
            saved_times[diff] += 1

# pprint(saved_times)

total_at_least_hundred = 0
for time_saved, count in saved_times.items():
    if time_saved >= 100:
        total_at_least_hundred += count

print(f"{total_at_least_hundred} cheats save at least 100pS")
