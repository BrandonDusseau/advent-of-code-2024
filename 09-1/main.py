import os
from pprint import pprint

with open(os.path.join(os.path.dirname(__file__), "input.txt")) as f:
    lines = f.readlines()

map = list(lines[0].strip())
data = []
free_space = []
file_id = 0
processing_file = True
# Read the input
for i in range(0, len(map)):
    if processing_file:
        for j in range(0, int(map[i])):
            data.append(str(file_id))
        file_id += 1
    else:
        for j in range(0, int(map[i])):
            free_space.append(len(data))
            data.append('.')
    processing_file = not processing_file

# Move data into free space
expected_data_size = len(data) - len(free_space)
last_index_after_compacting = expected_data_size - 1
for i in range(len(data) - 1, last_index_after_compacting, -1):
    if len(free_space) == 0:
        break
    if data[i] != '.':
        next_free_space = free_space.pop(0)
        data[next_free_space] = data[i]
        data[i] = '.'

# Compute checksum
checksum = 0
for i in range(0, expected_data_size):
    checksum += i * int(data[i])

print(checksum)
