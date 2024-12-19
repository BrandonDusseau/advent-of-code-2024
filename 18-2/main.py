import math
import os
from pprint import pprint


def visualize(corrupted_bytes, memory_size):
    for y in range(0, memory_size + 1):
        row = []
        for x in range(0, memory_size + 1):
            row.append('#' if (x, y) in corrupted_bytes else '.')
        print(''.join(row))


def get_valid_neighbors(point, corrupted_bytes, memory_size, max_corrupted_bytes):
    x, y = point
    potential_neighbors = []
    if x > 0:
        potential_neighbors.append((x - 1, y))
    if y > 0:
        potential_neighbors.append((x, y - 1))
    if x < memory_size:
        potential_neighbors.append((x + 1, y))
    if y < memory_size:
        potential_neighbors.append((x, y + 1))

    return [x for x in potential_neighbors if x not in corrupted_bytes[:max_corrupted_bytes]]


def dijkstra_shortest_path_length(corrupted_bytes, memory_size, max_corrupted_bytes):
    corrupted_bytes_subset = corrupted_bytes[:max_corrupted_bytes]
    start = (0, 0)
    target = (memory_size, memory_size)

    dist = {}
    prev = {}
    q = set()
    for y in range(0, memory_size + 1):
        for x in range(0, memory_size + 1):
            point = (x, y)
            if point in corrupted_bytes_subset:
                continue
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

        if u == target and dist[u] != math.inf:
            return dist[u]

        q.remove(u)

        neighbors = get_valid_neighbors(u, corrupted_bytes, memory_size, max_corrupted_bytes)
        for v in neighbors:
            if v not in q:
                continue

            alt = dist[u] + 1
            if alt < dist[v]:
                dist[v] = alt
                prev[v] = u

    return None


def find_first_failure(corrupted_bytes, memory_size, start):
    lower_bound = start
    upper_bound = len(corrupted_bytes) - 1

    while lower_bound != upper_bound:
        check_point = lower_bound + ((upper_bound - lower_bound) // 2)
        # print(f"Lower: {lower_bound}, Upper: {upper_bound}, Check: {check_point}")
        result = dijkstra_shortest_path_length(corrupted_bytes, memory_size, check_point)
        # visualize(corrupted_bytes[:check_point], memory_size)
        if result is None:
            upper_bound = check_point
            # print(f"  Failed to find exit - moving upper bound to {upper_bound}")
        else:
            lower_bound = check_point + 1
            # print(f"  Found exit - moving to lower bound to {lower_bound}")

    return corrupted_bytes[lower_bound - 1]


with open(os.path.join(os.path.dirname(__file__), "input.txt")) as f:
    lines = f.readlines()

memory_size = 70
known_starting_point = 1024
corrupted_bytes = []
for line in lines:
    stripped_line = line.strip()
    if line == '':
        continue
    x, y = stripped_line.split(',')
    corrupted_bytes.append((int(x), int(y)))

result_x, result_y = find_first_failure(corrupted_bytes, memory_size, known_starting_point)
print(f"{result_x},{result_y}")
