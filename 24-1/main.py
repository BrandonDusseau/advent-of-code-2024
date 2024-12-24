import os
from collections import defaultdict
from pprint import pprint


class Gate(object):
    def __init__(self, in_1, in_2, operator, out):
        self.in_1 = in_1
        self.in_2 = in_2
        self.operator = operator
        self.out = out

    def execute(self, wires, locked_gates):
        if self.in_1 not in wires or self.in_2 not in wires:
            return

        if self in locked_gates:
            return

        if self.operator == 'AND':
            wires[self.out] = 1 if wires[self.in_1] == 1 and wires[self.in_2] == 1 else 0
        elif self.operator == 'OR':
            wires[self.out] = 1 if wires[self.in_1] == 1 or wires[self.in_2] == 1 else 0
        elif self.operator == 'XOR':
            wires[self.out] = 1 if wires[self.in_1] != wires[self.in_2] else 0

        locked_gates.add(self)

    def __repr__(self):
        return f"{self.in_1} {self.operator} {self.in_2} -> {self.out}"


with open(os.path.join(os.path.dirname(__file__), "input.txt")) as f:
    lines = f.readlines()

wires = defaultdict(int)
gates = []
locked_gates = set()
reading_wires = True
for line in lines:
    stripped_line = line.strip()
    if stripped_line == '':
        reading_wires = False
        continue
    if reading_wires:
        wire, value = stripped_line.split(': ')
        wires[wire] = int(value)
    else:
        in_1, operator, in_2, _, out = stripped_line.split(' ')
        gates.append(Gate(in_1, in_2, operator, out))

while len(locked_gates) != len(gates):
    for gate in gates:
        gate.execute(wires, locked_gates)

z_wire_keys = [x for x in sorted(wires.keys(), reverse=True) if x.startswith('z')]
z_wire_values = [wires[x] for x in z_wire_keys]

end_value = 0
for z_wire_value in z_wire_values:
    end_value = (end_value << 1) | z_wire_value

print(end_value)
