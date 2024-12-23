import os
from pprint import pprint


class Computer(object):
    def __init__(self, name):
        self.name = name
        self.connected_to = set()

    def __repr__(self):
        return f"{self.name} connected to [{', '.join([x.name for x in self.connected_to])}]"


with open(os.path.join(os.path.dirname(__file__), "input.txt")) as f:
    lines = f.readlines()

computers = {}
for line in lines:
    stripped_line = line.strip()
    (computer_1, computer_2) = stripped_line.split('-')
    if computer_1 not in computers:
        computers[computer_1] = Computer(computer_1)
    if computer_2 not in computers:
        computers[computer_2] = Computer(computer_2)

    if computers[computer_2] not in computers[computer_1].connected_to:
        computers[computer_1].connected_to.add(computers[computer_2])

    if computers[computer_1] not in computers[computer_2].connected_to:
        computers[computer_2].connected_to.add(computers[computer_1])

groups_of_three = set()
for computer in computers.values():
    for neighbor_1 in computer.connected_to:
        for neighbor_2 in computer.connected_to:
            if neighbor_1 == neighbor_2:
                continue
            if neighbor_1 in neighbor_2.connected_to and (computer.name[0] == 't' or neighbor_1.name[0] == 't' or neighbor_2.name[0] == 't'):
                groups_of_three.add(','.join(sorted([computer.name, neighbor_1.name, neighbor_2.name])))

pprint(groups_of_three)

print(len(groups_of_three))
