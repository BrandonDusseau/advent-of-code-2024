import os
from pprint import pprint


num_button_positions = {
    'A': (2, 3),
    '0': (1, 3),
    '3': (2, 2),
    '2': (1, 2),
    '1': (0, 2),
    '6': (2, 1),
    '5': (1, 1),
    '4': (0, 1),
    '9': (2, 0),
    '8': (1, 0),
    '7': (0, 0),
}

dir_button_positions = {
    '>': (2, 1),
    'v': (1, 1),
    '<': (0, 1),
    'A': (2, 0),
    '^': (1, 0)
}

def get_movements_to_number(current_position, target):
    target_position = num_button_positions[target]
    vert_diff = target_position[1] - current_position[1]
    horiz_diff = target_position[0] - current_position[0]

    is_positioned_at_1 = current_position == num_button_positions['1']

    directions = []
    # If the arm is positioned at 1, horizontal movement needs to happen virst to avoid
    # the gap. If positioned at 0, vertical movement will already occur first and avoid this.
    if not is_positioned_at_1:
        if vert_diff < 0:
            directions += list('^' * -vert_diff)
        elif vert_diff > 0:
            directions += list('v' * vert_diff)

    if horiz_diff < 0:
        directions += list('<' * -horiz_diff)
    elif horiz_diff > 0:
        directions += list('>' * horiz_diff)

    if is_positioned_at_1:
        if vert_diff < 0:
            directions += list('^' * -vert_diff)
        elif vert_diff > 0:
            directions += list('v' * vert_diff)

    directions.append('A')

    return directions


def get_movements_to_direction(current_position, target):
    target_position = dir_button_positions[target]
    vert_diff = target_position[1] - current_position[1]
    horiz_diff = target_position[0] - current_position[0]

    is_positioned_at_right = current_position == dir_button_positions['<']

    directions = []
    # If the arm is positioned at <, horizontal movement needs to happen virst to avoid
    # the gap. If positioned at ^, vertical movement will already occur first and avoid this.
    if not is_positioned_at_right:
        if vert_diff < 0:
            directions += list('^' * -vert_diff)
        elif vert_diff > 0:
            directions += list('v' * vert_diff)

    if horiz_diff < 0:
        directions += list('<' * -horiz_diff)
    elif horiz_diff > 0:
        directions += list('>' * horiz_diff)

    if is_positioned_at_right:
        if vert_diff < 0:
            directions += list('^' * -vert_diff)
        elif vert_diff > 0:
            directions += list('v' * vert_diff)

    directions.append('A')

    return directions


with open(os.path.join(os.path.dirname(__file__), "input.txt")) as f:
    lines = f.readlines()

code_numbers = []
codes = []
for line in lines:
    stripped_line = line.strip()
    codes.append(list(stripped_line))
    code_numbers.append(int(stripped_line[:-1]))

num_keypad_position = num_button_positions['A']
dir_keypad_1_position = dir_button_positions['A']
dir_keypad_2_position = dir_button_positions['A']

complexity_sum = 0
for code_index in range(0, len(codes)):
    code = codes[code_index]
    code_number = code_numbers[code_index]
    print()

    num_movements = []
    for num_button in code:
        num_movements += get_movements_to_number(num_keypad_position, num_button)
        num_keypad_position = num_button_positions[num_button]
    print(''.join(num_movements))

    keypad_1_movements = []
    for dir_button in num_movements:
        keypad_1_movements += get_movements_to_direction(dir_keypad_1_position, dir_button)
        dir_keypad_1_position = dir_button_positions[dir_button]
    print(''.join(keypad_1_movements))

    keypad_2_movements = []
    for dir_button in keypad_1_movements:
        next_movements = get_movements_to_direction(dir_keypad_2_position, dir_button)
        keypad_2_movements += next_movements
        dir_keypad_2_position = dir_button_positions[dir_button]
    print(''.join(keypad_2_movements))

    complexity = len(keypad_2_movements) * code_number
    print(f"Code {''.join(code)}: Sequence length {len(keypad_2_movements)}; Complexity {complexity}")
    complexity_sum += complexity

print(complexity_sum)
