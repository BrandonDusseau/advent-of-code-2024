import re
import os
from pprint import pprint

with open(os.path.join(os.path.dirname(__file__), "input.txt")) as f:
    lines = f.readlines()

left_numbers = []
right_occurrences = {}
for line in lines:
    strippedLine = line.strip()
    if strippedLine == "":
        continue

    match = re.match(r"^(\d+)\s+(\d+)", line)
    if match is None:
        continue

    left_numbers.append(int(match.groups()[0]))
    right_number = int(match.groups()[1])
    if right_number in right_occurrences:
        right_occurrences[right_number] += 1
    else:
        right_occurrences[right_number] = 1

similarity_score = 0
for left_number in left_numbers:
    if left_number not in right_occurrences:
        continue
    similarity_score += left_number * right_occurrences[left_number]

print(similarity_score)
