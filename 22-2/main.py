import os
from pprint import pprint


def get_next_secret_number(secret_number):
    next_secret = ((secret_number * 64) ^ secret_number) % 16777216
    next_secret = ((next_secret // 32) ^ next_secret) % 16777216
    next_secret = ((next_secret * 2048) ^ next_secret) % 16777216
    return next_secret


with open(os.path.join(os.path.dirname(__file__), "input.txt")) as f:
    lines = f.readlines()

secret_numbers = []
for line in lines:
    stripped_line = line.strip()
    if stripped_line == '':
        continue
    secret_numbers.append(int(stripped_line))

sequences = {}

for number in secret_numbers:
    this_number = number
    last_price = int(str(this_number)[-1])
    changes_window = []
    secret_numbers = []
    seen_sequences = {}

    for i in range(0, 2000):
        this_number = get_next_secret_number(this_number)
        new_price = int(str(this_number)[-1])

        changes_window.append(new_price - last_price)
        if len(changes_window) > 4:
            changes_window.pop(0)

        if len(changes_window) == 4:
            sequence_string = "|".join([str(x) for x in changes_window])
            if sequence_string not in seen_sequences:
                seen_sequences[sequence_string] = new_price
        last_price = new_price

    for sequence, price in seen_sequences.items():
        if sequence in sequences:
            sequences[sequence] += price
        else:
            sequences[sequence] = price

print(max(sequences.values()))
