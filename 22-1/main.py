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

sum_of_2000 = 0
for number in secret_numbers:
    this_number = number
    for i in range(0, 2000):
        this_number = get_next_secret_number(this_number)

    sum_of_2000 += this_number

print(sum_of_2000)

