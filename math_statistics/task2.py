import numpy as np
import matplotlib.pyplot as plt
import math


with open('exponentials.csv', 'r') as file:
    lines = file.read().split('\n')
    data = []
    for line in lines:
        if line == '':
            continue
        data.append(list(float(s) for s in line.split(',')))

n = 5

data = np.array(data)
groups = []
thetas = []
for i in range(1, n + 1):
    group = data[data[:, 0] == i]
    g1 = group[:, 1]
    g2 = group[:, 2]
    groups.append((g1, g2))
    theta1 = np.mean(g1)
    theta2 = np.mean(g2)
    thetas.append((theta1, theta2))

# print(groups)
print(thetas)

pairs = set()
for i in range(1, n + 1):
    for j in range(1, n + 1):
        if i != j:
            pairs.add((min(i, j), max(i, j)))

pairs = sorted(list(pairs))
print(pairs)


def get_probability(noise : bool, e : float):
    for pair in pairs:
        i, j = pair
        theta1 = thetas[i-1][0 if not noise else 1]
        theta2 = thetas[j-1][0 if not noise else 1]
        D1 = theta1 ** 2 / groups[i-1][0 if not noise else 1].shape[0]
        D2 = theta2 ** 2 / groups[j-1][0 if not noise else 1].shape[0]

        D_delta = D1 + D2
        # print('d_delta', D_delta)
        P = min(1, D_delta / (e ** 2))

        print('without noise' if not noise else 'with noise')
        print(f'pair {pair}, theta_1 = {round(theta1, 3)}, theta_2 = {round(theta2, 3)}, D1 = {round(D1, 3)}, D2 = {round(D2, 3)}')
        print(f'P(|theta1 - theta2| >= e) <= {round(P, 5)}\n')
    

e = 200
get_probability(False, e)
get_probability(True, e)
