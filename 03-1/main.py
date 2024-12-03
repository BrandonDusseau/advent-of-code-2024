import re
import os
from pprint import pprint

with open(os.path.join(os.path.dirname(__file__), "input.txt")) as f:
    lines = f.readlines()

memory = ''.join(lines)
matches = re.findall(r"mul\((\d+),(\d+)\)", memory)
products = list(map(lambda match:int(match[0]) * int(match[1]), matches))

print(sum(products))
