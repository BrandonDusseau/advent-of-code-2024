import os
from pprint import pprint


with open(os.path.join(os.path.dirname(__file__), "input.txt")) as f:
    line = f.readline()

stones = [int(x) for x in line.strip().split(' ')]


def transform_stone(stone):
    new_stones = []
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

    return new_stones


def cache_stone(stone, layer_cache):
    stone_set = [stone]
    for i in range(0, 5):
        next_set = []
        for next_stone in stone_set:
            next_set += transform_stone(next_stone)
        layer_cache[(stone, i + 1)] = next_set
        stone_set = next_set


def process_stone(stone, current_blink, layer_cache):
    max_blinks = 75

    if (stone, 1) not in layer_cache:
        cache_stone(stone, layer_cache)
    next_set = layer_cache[(stone, 1)]

    if current_blink == max_blinks:
        return len(next_set)

    sum = 0
    for next_stone in next_set:
        if (next_stone, 1) not in layer_cache:
            cache_stone(next_stone, layer_cache)
        blinks_left = max_blinks - current_blink
        blinks_to_skip = min(blinks_left, 5)

        for next_stone_skip in layer_cache[(next_stone, blinks_to_skip - 1)]:
            sum += process_stone(next_stone_skip, current_blink + blinks_to_skip, layer_cache)

    return sum


stone_memo = {}
layer_cache = {}
sum = 0
for this_stone in stones:
    sum += process_stone(this_stone, 1, layer_cache)

print(sum)
