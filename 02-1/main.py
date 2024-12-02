import re
import os
from pprint import pprint

with open(os.path.join(os.path.dirname(__file__), "input.txt")) as f:
    lines = f.readlines()

reports = []
for line in lines:
    strippedLine = line.strip()
    if strippedLine == "":
        continue

    reports.append(list(map(lambda x:int(x), strippedLine.split(' '))))

safe_reports = 0

for report in reports:
    should_be_increasing = report[1] > report[0]
    is_safe = True
    for index in range(1, len(report)):
        diff = abs(report[index] - report[index - 1])
        is_increasing = report[index] > report[index - 1]
        if diff < 1 or diff > 3 or is_increasing != should_be_increasing:
            is_safe = False
            break
    if is_safe:
        safe_reports += 1

print(safe_reports)
