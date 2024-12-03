import re
import os
from pprint import pprint

with open(os.path.join(os.path.dirname(__file__), "input.txt")) as f:
    lines = f.readlines()

memory = ''.join(lines)

reduced_memory = ""
# Split memory by don't(). The first segment is always enabled because it's before "don't()".
# The segment between "don't()" and "do()" (always the first segment when splitting by do())
# is disabled, so discard it.
# Recombine all the segments and then scan for mul() commands.
memory_segments = memory.split("don't()")
reduced_memory = memory_segments.pop(0)
for segment in memory_segments:
    reduced_memory += ''.join(segment.split("do()")[1:])

matches = re.findall(r"mul\((\d+),(\d+)\)", reduced_memory)
products = list(map(lambda match:int(match[0]) * int(match[1]), matches))

print(sum(products))
