import re
import os
from pprint import pprint

def check_report(report):
    previous_increase_value = report[1] > report[0]
    problem_indices = []
    for index in range(1, len(report)):
        diff = abs(report[index] - report[index - 1])
        is_increasing = report[index] > report[index - 1]
        print(f"  {report[index - 1]} {report[index]} Diff: {diff} Increase: {is_increasing}")
        if diff < 1 or diff > 3 or is_increasing != previous_increase_value:
            problem_indices.append(index)
        previous_increase_value = is_increasing

    return problem_indices

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
    pprint(report)
    is_safe = False

    problems = check_report(report)
    if len(problems) == 0:
        print("Safe\n")
        safe_reports += 1
        continue

    # Try to recover by testing the removal of each index.
    for removed_index in range(0, len(report)):
        print(f"Checking again removing {removed_index}")
        new_problems = check_report([x for i,x in enumerate(report) if i!=removed_index])
        if len(new_problems) == 0:
            print(f"Safe by removing index {removed_index}\n")
            safe_reports += 1
            break

    print("Unsafe\n")

print(safe_reports)
