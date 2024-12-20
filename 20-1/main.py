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
for line_index in range(0, len(lines) - 1):
    if line_index == 0:
        continue

    line = lines[line_index].strip()

    if line == '':
        continue

    max_y += 1
    max_x = len(line) - 3
    for col_index in range(1, len(line) - 1):
        x = col_index - 1
        point = (x, max_y)
        char = line[col_index]
        if char == 'S':
            start = point
        if char == 'E':
            end = point
        if char == '#':
            walls.add(point)
        if char in {'S', 'E', '.'}:
            spaces.add(point)

# Find which walls will have an effect if they are removed.
removable_walls = set()
cheats = set()
for wall in walls:
    adjacent_points = get_surrounding_points(wall)
    adjacent_spaces = [x for x in adjacent_points if x in spaces]
    adjacent_walls = [x for x in adjacent_points if x in walls]

    # The wall is only useful if it touches at least one open space.
    if len(adjacent_spaces) >= 1:
        removable_walls.add(wall)

    # The wall is a candidate to be removed by itself if it touches at least two spaces.
    if len(adjacent_spaces) >= 2:
        cheats.add(wall)


# visualize(spaces, walls, start, end, max_x, max_y)

dist_from_start, prev_data = dijkstra(spaces, start)
base_time = dist_from_start[end]
print(f"Base time: {base_time} pS")
print(f"There are {len(cheats)} cheats")

original_path = []
u = end
if u in prev_data or u == start:
    while u is not None:
        original_path.insert(0, u)
        u = prev_data[u]

dist_from_end, _ = dijkstra(spaces, end)

saved_times = {}
for point in original_path:
    # Get cheats adjacent to this point.
    surrounding_cheats = [x for x in get_surrounding_points(point) if x in cheats]
    cost_to_this_point = dist_from_start[point]
    for cheat in surrounding_cheats:
        # Get other spaces that this point would connect to.
        connections = [x for x in get_surrounding_points(cheat) if x in spaces and x != point]
        max_diff_for_this_cheat = 0
        for connection in connections:
            # The calculated distance assumes the first point isn't a movement, so add an extra 1.
            cost_from_connection_to_end = dist_from_end[connection] + 1
            # Add another 1 for the movement through the wall.
            total_time = cost_to_this_point + cost_from_connection_to_end + 1

            diff = base_time - total_time
            if diff > max_diff_for_this_cheat:
                max_diff_for_this_cheat = diff

        if max_diff_for_this_cheat <= 0:
            continue

        if max_diff_for_this_cheat not in saved_times:
            saved_times[max_diff_for_this_cheat] = 1
        else:
            saved_times[max_diff_for_this_cheat] += 1

pprint(saved_times)
print(f"{saved_times.get(100, 0)} cheats save 100pS")
