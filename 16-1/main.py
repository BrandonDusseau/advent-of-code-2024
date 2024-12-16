import math
import os
from pprint import pprint


class Node(object):
    def __init__(self, col, row):
        self.col = col
        self.row = row
        self.neighbors = {'n': None, 'e': None, 's': None, 'w': None}

    def __repr__(self):
        return f"({self.col}, {self.row})"

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

for node in positions.values():
    print(f"{node.get_point_string()} - Neighbors: [{node.get_neighbors_string()}]")

pprint(a_star(start, end, heuristic, positions))
