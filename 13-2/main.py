import os
import re
from pprint import pprint


class Machine(object):
    def __init__(self, button_a_x, button_a_y, button_b_x, button_b_y, prize_x, prize_y):
        self.button_a_x = button_a_x
        self.button_a_y = button_a_y
        self.button_b_x = button_b_x
        self.button_b_y = button_b_y
        self.prize_x = prize_x + 10000000000000
        self.prize_y = prize_y + 10000000000000

    def __repr__(self):
        return f"Button A: X+{self.button_a_x}, Y+{self.button_a_y}; Button B: X+{self.button_b_x}, Y+{self.button_b_y}; Prize: X={self.prize_x}, Y={self.prize_y}"


with open(os.path.join(os.path.dirname(__file__), "input.txt")) as f:
    lines = f.readlines()

machines = []
for i in range(0, len(lines), 4):
    (button_a_x, button_a_y) = [int(x) for x in re.match(r"Button A: X\+(\d+), Y\+(\d+)", lines[i]).groups()]
    (button_b_x, button_b_y) = [int(x) for x in re.match(r"Button B: X\+(\d+), Y\+(\d+)", lines[i + 1]).groups()]
    (goal_x, goal_y) = [int(x) for x in re.match(r"Prize: X=(\d+), Y=(\d+)", lines[i + 2]).groups()]
    machines.append(Machine(button_a_x, button_a_y, button_b_x, button_b_y, goal_x, goal_y))

sum = 0
for machine in machines:
    print(f"Processing machine [{machine}]")
    b_presses = ((machine.button_a_y * machine.prize_x) - (machine.button_a_x * machine.prize_y)) / (-(machine.button_a_x * machine.button_b_y) + (machine.button_a_y * machine.button_b_x))
    a_presses = (machine.prize_x - (b_presses * machine.button_b_x)) / machine.button_a_x

    print(f"  A presses: {a_presses}, B presses: {b_presses}")

    if b_presses % 1 != 0 or a_presses % 1 != 0:
        print("  Can't win a prize")
    else:
        tokens = (a_presses * 3) + b_presses
        print(f"  Tokens needed: {tokens}")
        sum += int(tokens)

print(sum)
