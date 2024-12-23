import os
from collections import defaultdict
from pprint import pprint


# https://github.com/alanmc-zz/python-bors-kerbosch/blob/master/bors-kerbosch.py
def bors_kerbosch_v2(R, P, X, G, C):
    if len(P) == 0 and len(X) == 0:
        if len(R) > 2:
            C.append(sorted(R))
        return

    (d, pivot) = max([(len(G[v]), v) for v in P.union(X)])

    for v in P.difference(G[pivot]):
        bors_kerbosch_v2(R.union(set([v])), P.intersection(G[v]), X.intersection(G[v]), G, C)
        P.remove(v)
        X.add(v)


with open(os.path.join(os.path.dirname(__file__), "input.txt")) as f:
    lines = f.readlines()

computers = defaultdict(set)
for line in lines:
    stripped_line = line.strip()
    (computer_1, computer_2) = stripped_line.split('-')
    computers[computer_1].add(computer_2)
    computers[computer_2].add(computer_1)

networks = []
bors_kerbosch_v2(set([]), set(computers.keys()), set([]), computers, networks)

network_strings = []
for network in networks:
    network_strings.append(','.join(sorted(network)))

ordered_networks = sorted(network_strings, key=lambda k: len(k), reverse=True)
print(ordered_networks[0])
