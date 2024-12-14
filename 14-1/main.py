import math
import os
import re
from pprint import pprint


class Robot(object):
    def __init__(self, pos_x, pos_y, velocity_x, velocity_y):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.velocity_x = velocity_x
        self.velocity_y = velocity_y

    def __repr__(self):
        return f"Position: ({self.pos_x}, {self.pos_y}); Velocity: ({self.velocity_x}, {self.velocity_y})"


with open(os.path.join(os.path.dirname(__file__), "input.txt")) as f:
    lines = f.readlines()

robots = []
for line in lines:
    (pos_x, pos_y, vel_x, vel_y) = [int(x) for x in re.match(r"p=(\d+),(\d+) v=(-?\d+),(-?\d+)", line).groups()]
    robots.append(Robot(pos_x, pos_y, vel_x, vel_y))

width = 101
height = 103

quadrants = [0, 0, 0, 0]
for robot in robots:
    final_pos_x = (robot.pos_x + (robot.velocity_x * 100)) % width
    final_pos_y = (robot.pos_y + (robot.velocity_y * 100)) % height

    if final_pos_x == width // 2 or final_pos_y == height // 2:
        continue

    base_quadrant = 1 if final_pos_x > width // 2 else 0
    quadrant_offset = 2 if final_pos_y > height // 2 else 0
    quadrant_index = base_quadrant + quadrant_offset
    quadrants[quadrant_index] += 1

pprint(quadrants)
print(math.prod(quadrants))
