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


def get_output_dependencies(out, gates_by_output):
    if out not in gates_by_output:
        return set()

    this_gate = gates_by_output[out]
    in_1_dependencies = get_output_dependencies(this_gate.in_1, gates_by_output)
    in_2_dependencies = get_output_dependencies(this_gate.in_2, gates_by_output)
    return {this_gate}.union(in_1_dependencies).union(in_2_dependencies)


with open(os.path.join(os.path.dirname(__file__), "input.txt")) as f:
    lines = f.readlines()

wires = {}
gates = []
gates_by_output = {}
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
        gate = Gate(in_1, in_2, operator, out)
        gates.append(gate)
        gates_by_output[out] = gate

x_wire_keys = [x for x in sorted(wires.keys(), reverse=True) if x.startswith('x')]
y_wire_keys = [x for x in sorted(wires.keys(), reverse=True) if x.startswith('y')]
x_wire_values = [wires[x] for x in x_wire_keys]
y_wire_values = [wires[x] for x in y_wire_keys]

original_x_value = 0
for x_wire_value in x_wire_values:
    original_x_value = (original_x_value << 1) | x_wire_value

original_y_value = 0
for y_wire_value in y_wire_values:
    original_y_value = (original_y_value << 1) | y_wire_value

correct_z_value = original_x_value + original_y_value
z_value_temp = correct_z_value
correct_z_wire_values = []
while z_value_temp != 0:
    correct_z_wire_values.insert(0, z_value_temp & 1)
    z_value_temp >>= 1

z_wire_keys = [x for x in sorted(gates_by_output.keys(), reverse=True) if x.startswith('z')]
correct_z_wire_values = correct_z_wire_values[0:len(z_wire_keys)]

print(original_x_value)
print(original_y_value)
print(correct_z_value)

locked_gates = set()
while len(locked_gates) != len(gates):
    for gate in gates:
        gate.execute(wires, locked_gates)

z_wire_values = [wires[x] for x in z_wire_keys]

incorrect_z_value = 0
for z_wire_value in z_wire_values:
    incorrect_z_value = (incorrect_z_value << 1) | z_wire_value

length_diff = len(z_wire_values) - len(correct_z_wire_values)
if length_diff != 0:
    for i in range(0, length_diff):
        correct_z_wire_values.append(0)

print(x_wire_values)
print(y_wire_values)
print(z_wire_values)
print(correct_z_wire_values)

incorrect_z_wires = []
for i in range(0, len(z_wire_values)):
    if z_wire_values[i] != correct_z_wire_values[i]:
        incorrect_z_wires.append(z_wire_keys[i])

dependency_sets = []
for incorrect_z_wire in incorrect_z_wires:
    dependency_sets.append(get_output_dependencies(incorrect_z_wire, gates_by_output))

# pprint(dependency_sets)

common_dependencies = set.intersection(*dependency_sets)
print(common_dependencies)
