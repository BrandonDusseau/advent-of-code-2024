import re
import os
from pprint import pprint

with open(os.path.join(os.path.dirname(__file__), "input.txt")) as f:
    lines = f.readlines()

memory = ''.join(lines)

keep = []
# Split memory by don't(). The first segment is always enabled because it's before "don't()".
# The segment between "don't()" and "do()" (always the first segment when splitting by do())
# is disabled, so discard it.
# Recombine all the segments and then scan for mul() commands.
dont_sections = memory.split("don't()")
keep.append(dont_sections.pop(0))
for section in dont_sections:
    keep = keep + section.split("do()")[1:]

memory = ''.join(keep)

matches = re.findall(r"mul\((\d+),(\d+)\)", memory)
products = list(map(lambda match:int(match[0]) * int(match[1]), matches))

print(sum(products))
