import os
from pprint import pprint


def move_file_to_first_open_space(file_id, data, file_positions, file_lengths, free_spaces):
    original_position = file_positions[file_id]
    file_length = file_lengths[file_id]

    for space_start in sorted(free_spaces):
        space_length = free_spaces[space_start]
        if space_start >= original_position:
            break
        if space_length >= file_length:
            # Move the physical file
            for offset in range(0, file_length):
                data[space_start + offset] = str(file_id)
                data[original_position + offset] = '.'

            # Update the file position metadata
            file_positions[file_id] = space_start

            # Adjust free space that might remain after where we just placed the file.
            remaining_free_space = space_length - file_length
            free_spaces.pop(space_start)
            if remaining_free_space > 0:
                free_spaces[space_start + file_length] = remaining_free_space

            # Adjust free space surrounding where the file was.
            new_free_space_start = original_position
            # If there was free space directly preceding the original file, expand it by the file length.
            # Otherwise, create new free space where the file was.
            if original_position != 0 and data[original_position - 1] == '.':
                preceding_free_space_start = original_position - 1
                while preceding_free_space_start - 1 != 0 and data[preceding_free_space_start - 1] == '.':
                    preceding_free_space_start -= 1
                new_free_space_start = preceding_free_space_start
                free_spaces[new_free_space_start] += file_length
            else:
                free_spaces[new_free_space_start] = file_length

            # If there was free space directly after the original file, merge it into the preceding free space.
            free_space_after_position = original_position + file_length
            if free_space_after_position in free_spaces:
                free_spaces[new_free_space_start] += free_spaces[free_space_after_position]
                free_spaces.pop(free_space_after_position)

            return True
    return False


with open(os.path.join(os.path.dirname(__file__), "input.txt")) as f:
    lines = f.readlines()

map = list(lines[0].strip())
data = []
file_position = {}
file_length = {}
free_space = {}

file_id = 0
processing_file = True
# Read the input
for i in range(0, len(map)):
    length = int(map[i])
    start_position = len(data)
    if processing_file:
        file_position[file_id] = start_position
        file_length[file_id] = length
        for j in range(0, length):
            data.append(str(file_id))
        file_id += 1
    else:
        free_space[start_position] = length
        for j in range(0, length):
            data.append('.')
    processing_file = not processing_file

# Move each file into the next available open space.
for move_file_id in range(file_id - 1, -1, -1):
    was_moved = move_file_to_first_open_space(move_file_id, data, file_position, file_length, free_space)
    # was_moved = move_file_to_first_open_space(move_file_id, data, file_position, file_length, free_space)
    # if was_moved:
    #     print(''.join(data))

# Compute checksum
checksum = 0
for i in range(0, len(data)):
    if data[i] == '.':
        continue
    checksum += i * int(data[i])

print(checksum)
