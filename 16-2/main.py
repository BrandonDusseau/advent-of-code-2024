import math
import os
from pprint import pprint


class Node(object):
    def __init__(self, col, row):
        self.col = col
        self.row = row
        self.neighbors = {'n': None, 'e': None, 's': None, 'w': None}

    def __repr__(self):
        return f"Node ({self.col}, {self.row})"

    def get_point_string(self):
        return self.__repr__()

    def get_neighbors_string(self):
        return ', '.join([f'{key}: {node.get_point_string()}' for key, node in self.neighbors.items() if node is not None])


def reconstruct_path(came_from, current):
    total_path = [current]
    while current in came_from.keys():
        current = came_from[current]
        total_path.insert(0, current)
    return total_path


def get_min_f_score_in_open_set(open_set, f_score):
    min_f_score = math.inf
    open_set_list = list(open_set)
    node_with_min_f_score = open_set_list[0]
    for open_set_item in open_set_list:
        node, _ = open_set_item
        if f_score[node] < min_f_score:
            min_f_score = f_score[node]
            node_with_min_f_score = open_set_item
    return node_with_min_f_score


def heuristic(node):
    return 1

def get_direction_weight(current_direction, next_direction):
    clockwise_weights = {
        'nn': 0,
        'ne': 1000,
        'ns': 2000,
        'nw': 3000,
        'ee': 0,
        'es': 1000,
        'ew': 2000,
        'en': 3000,
        'ss': 0,
        'sw': 1000,
        'sn': 2000,
        'se': 3000,
        'ww': 0,
        'wn': 1000,
        'we': 2000,
        'ws': 3000
    }

    counter_clockwise_weights = {
        'nn': 0,
        'nw': 1000,
        'ns': 2000,
        'ne': 3000,
        'ee': 0,
        'en': 1000,
        'ew': 2000,
        'es': 3000,
        'ss': 0,
        'se': 1000,
        'sn': 2000,
        'sw': 3000,
        'ww': 0,
        'ws': 1000,
        'we': 2000,
        'wn': 3000
    }

    key = f"{current_direction}{next_direction}"
    return min(clockwise_weights[key], counter_clockwise_weights[key])

def a_star(start, goal, h, positions):
    open_set = {(start, 'e')}
    came_from = {}

    g_score = {pos: math.inf for pos in positions.values()}
    g_score[start] = 0
    f_score = {pos: math.inf for pos in positions.values()}
    f_score[start] = h(start)

    while len(open_set) != 0:
        current = get_min_f_score_in_open_set(open_set, f_score)
        current_node, current_direction = current
        if current_node == goal:
            return reconstruct_path(came_from, current_node)

        open_set.remove(current)
        for neighbor_direction, neighbor_node in current_node.neighbors.items():
            if neighbor_node is None:
                continue
            tentative_g_score = g_score[current_node] + get_direction_weight(current_direction, neighbor_direction)
            if tentative_g_score < g_score[neighbor_node]:
                came_from[neighbor_node] = current_node
                g_score[neighbor_node] = tentative_g_score
                f_score[neighbor_node] = tentative_g_score + h(neighbor_node)
                if (neighbor_node, neighbor_direction) not in open_set:
                    open_set.add((neighbor_node, neighbor_direction))

    return None


def remove_neighbor(node, neighbor_to_remove):
    found = False
    for neighbor_direction, neighbor_node in node.neighbors.items():
            if neighbor_node == neighbor_to_remove:
                found = True
                break

    if not found:
        return None

    node.neighbors[neighbor_direction] = None
    return neighbor_direction


def score_path(path):
    current_point = path[0]
    current_direction = 'e'

    turn_penalty = 0
    move_cost = 0
    for point in path[1:]:
        for neighbor_direction, neighbor_node in current_point.neighbors.items():
            if neighbor_node == point:
                # print(f"Next node is ({point.col}, {point.row}) in direction {neighbor_direction}")
                turn_cost = get_direction_weight(current_direction, neighbor_direction)
                # print(f"  Add 1 move and {turn_cost} turn penalty")
                turn_penalty += turn_cost
                move_cost += 1
                current_point = point
                current_direction = neighbor_direction
                break

    return turn_penalty + move_cost

with open(os.path.join(os.path.dirname(__file__), "input.txt")) as f:
    lines = f.readlines()

start = None
end = None
deer_position = None
deer_direction = 'e'
positions = {}
for row in range(0, len(lines)):
    stripped_line = lines[row].strip()
    if stripped_line == '':
        continue
    for col in range(0, len(stripped_line)):
        char = stripped_line[col]
        point = Node(col, row)
        if char in {'S', 'E', '.'}:
            positions[(col, row)] = point
        if char == 'S':
            start = point
            deer_position = point
        if char == 'E':
            end = point

for point, node in positions.items():
    n = (point[0], point[1] - 1)
    e = (point[0] + 1, point[1])
    s = (point[0], point[1] + 1)
    w = (point[0] - 1, point[1])

    if n in positions.keys():
        node.neighbors['n'] = positions[n]
    if e in positions.keys():
        node.neighbors['e'] = positions[e]
    if s in positions.keys():
        node.neighbors['s'] = positions[s]
    if w in positions.keys():
        node.neighbors['w'] = positions[w]

path = a_star(start, end, heuristic, positions)
target_score = score_path(path)
paths = [path]
potential_kth_shortest_path = []

original_positions = positions.copy()

next_path_score = target_score
k = 1
while next_path_score == target_score:
    for i in range(0, len(paths[k - 1]) - 1):
        spur_node = paths[k - 1][i]
        root_path = paths[k - 1][:i + 1]

        removed_neighbors = []
        for path in paths:
            if root_path == path[:i + 1]:
                neighbor_direction_1 = remove_neighbor(path[i], path[i + 1])
                if neighbor_direction_1 is not None:
                    removed_neighbors.append((path[i], path[i + 1], neighbor_direction_1))
                neighbor_direction_2 = remove_neighbor(path[i + 1], path[i])
                if neighbor_direction_2 is not None:
                    removed_neighbors.append((path[i + 1], path[i], neighbor_direction_2))

        removed_nodes = []
        for node in root_path:
            if node == spur_node:
                continue

            # If we're deleting a node, delete all the edges to that node.
            for _, neighbor_node in node.neighbors.items():
                if neighbor_node is None:
                    continue

                neighbor_direction_1 = remove_neighbor(node, neighbor_node)
                if neighbor_direction_1 is not None:
                    removed_neighbors.append((node, neighbor_node, neighbor_direction_1))
                neighbor_direction_2 = remove_neighbor(neighbor_node, node)
                if neighbor_direction_2 is not None:
                    removed_neighbors.append((neighbor_node, node, neighbor_direction_2))
            del positions[(node.col, node.row)]
            removed_nodes.append(node)

        spur_path = a_star(spur_node, end, heuristic, positions)

        for node in removed_nodes:
            positions[(node.col, node.row)] = node
        removed_nodes = []
        for source, dest, direction in removed_neighbors:
            source.neighbors[direction] = dest
        removed_neighbors = []

        if spur_path is not None:
            total_path = root_path[:-1] + spur_path

            total_path_score = score_path(total_path)
            path_data = (total_path, total_path_score)
            if path_data not in potential_kth_shortest_path:
                potential_kth_shortest_path.append(path_data)

    if len(potential_kth_shortest_path) == 0:
        break

    # sort by the score
    sorted_potential_kth_shortest_path = sorted(potential_kth_shortest_path, key=lambda x: x[1])
    next_shortest_path = sorted_potential_kth_shortest_path[0]
    next_path_score = next_shortest_path[1]
    if next_path_score == target_score:
        paths.append(next_shortest_path[0])
    potential_kth_shortest_path = sorted_potential_kth_shortest_path[1:]

    k += 1

seats = set()
for path in paths:
    seats = seats.union(set(path))

print(len(seats))


