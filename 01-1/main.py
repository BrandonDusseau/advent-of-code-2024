import re
import os
from pprint import pprint

with open(os.path.join(os.path.dirname(__file__), "input.txt")) as f:
    lines = f.readlines()

left_numbers = []
right_numbers = []
for line in lines:
    strippedLine = line.strip()
    if strippedLine == "":
        continue

    match = re.match(r"^(\d+)\s+(\d+)", line)
    if match is None:
        continue

    left_numbers.append(int(match.groups()[0]))
    right_numbers.append(int(match.groups()[1]))

left_numbers.sort()
right_numbers.sort()

total_distance = 0
for i in range(0, len(left_numbers)):
    total_distance += abs(right_numbers[i] - left_numbers[i])

print(total_distance)
