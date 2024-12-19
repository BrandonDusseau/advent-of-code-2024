import math
import os
from pprint import pprint


def get_valid_neighbors(point, corrupted_bytes, memory_size):
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

    return [x for x in potential_neighbors if x not in corrupted_bytes]


def dijkstra_shortest_path_length(corrupted_bytes, memory_size):
    start = (0, 0)
    target = (memory_size, memory_size)

    dist = {}
    prev = {}
    q = set()
    for y in range(0, memory_size + 1):
        for x in range(0, memory_size + 1):
            point = (x, y)
            if point in corrupted_bytes:
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

        if u == target:
            return dist[u]

        q.remove(u)

        neighbors = get_valid_neighbors(u, corrupted_bytes, memory_size)
        for v in neighbors:
            if v not in q:
                continue

            alt = dist[u] + 1
            if alt < dist[v]:
                dist[v] = alt
                prev[v] = u

    return None


with open(os.path.join(os.path.dirname(__file__), "input.txt")) as f:
    lines = f.readlines()

memory_size = 70
max_corrupted_bytes = 1024
corrupted_bytes = set()
current_byte = 0
for line in lines:
    stripped_line = line.strip()
    if line == '':
        continue

    if current_byte >= max_corrupted_bytes:
        break
    current_byte += 1
    x, y = stripped_line.split(',')
    corrupted_bytes.add((int(x), int(y)))

result = dijkstra_shortest_path_length(corrupted_bytes, memory_size)
print(result)
