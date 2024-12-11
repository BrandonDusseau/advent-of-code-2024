import os
from pprint import pprint


with open(os.path.join(os.path.dirname(__file__), "input.txt")) as f:
    line = f.readline()

stones = [int(x) for x in line.strip().split(' ')]

for i in range (0, 25):
    new_stones = []
    for stone in stones:
        stone_string = str(stone)
        stone_digits = len(stone_string)
        if stone == 0:
            new_stones.append(1)
        elif stone_digits % 2 == 0:
            half_length = stone_digits // 2
            new_stones.append(int(stone_string[0:half_length]))
            new_stones.append(int(stone_string[half_length:]))
        else:
            new_stones.append(stone * 2024)
    stones = new_stones

print(len(stones))
