import os
import re
from collections import defaultdict
from pprint import pprint

class Robot(object):
    def __init__(self, pos_x, pos_y, velocity_x, velocity_y):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.velocity_x = velocity_x
        self.velocity_y = velocity_y

    def __repr__(self):
        return f"Position: ({self.pos_x}, {self.pos_y}); Velocity: ({self.velocity_x}, {self.velocity_y})"


def visualize(robot_positions, width, height):
    for row in range(0, height):
        row_chars = []
        for col in range(0, width):
            point = (col, row)
            if point in robot_positions:
                row_chars.append(str(robot_positions[point]))
            else:
                row_chars.append('.')
        print(''.join(row_chars))


with open(os.path.join(os.path.dirname(__file__), "input.txt")) as f:
    lines = f.readlines()

robots = []
robot_positions = defaultdict(int)
for line in lines:
    (pos_x, pos_y, vel_x, vel_y) = [int(x) for x in re.match(r"p=(\d+),(\d+) v=(-?\d+),(-?\d+)", line).groups()]
    robots.append(Robot(pos_x, pos_y, vel_x, vel_y))
    robot_positions[(pos_x, pos_y)] += 1

width = 101
height = 103

print("0")
visualize(robot_positions, width, height)
print()

cache = set()
i = 0
while True:
    i += 1
    robot_positions = defaultdict(int)
    for robot in robots:
        robot.pos_x = (robot.pos_x + (robot.velocity_x)) % width
        robot.pos_y = (robot.pos_y + (robot.velocity_y)) % height
        robot_positions[(robot.pos_x, robot.pos_y)] += 1

    positions = []
    for key, quantity in robot_positions.items():
        for q in range(0, quantity):
            positions.append(key)
    cache_key = "|".join(sorted([f"{col},{row}" for col, row in positions]))

    if cache_key in cache:
        break
    cache.add(cache_key)

    print(i)
    visualize(robot_positions, width, height)
    print()

print(f"Cycle detected after {i} seconds")
# robot_positions = defaultdict(int)
# for robot in robots:
#     robot.pos_x = (robot.pos_x + (robot.velocity_x * (i - 1))) % width
#     robot.pos_y = (robot.pos_y + (robot.velocity_y * (i - 1))) % height
#     robot_positions[(robot.pos_x, robot.pos_y)] += 1
# visualize(robot_positions, width, height)
