import numpy as np
import matplotlib.pyplot as plt


n = 10

with open('mean-median.csv', 'r') as file:
    lines = file.read().split('\n')
    data = []
    for line in lines:
        if line == '':
            continue
        data.append(list(float(s) for s in line.split(',')))

data = np.array(data)
data = data[data[:, 0] == 5.0]
data = data[:, 1:]

sz = int(round(data.shape[0] / n))

means = []
meds = []
quantiles = []
q_values = [0.2, 0.4, 0.6, 0.8]

for i in range(n):
    group = data[i*sz:(i+1)*sz]
    mean = np.mean(group, axis=0)
    means.append(mean)
    med = np.median(group, axis=0)
    meds.append(med)
    q = [np.quantile(group, q, axis=0) for q in q_values]
    quantiles.append(q)
    
print(f'means = {means}')
print(f'meds = {meds}')
print(f'quantiles = {quantiles}')

means = np.array(means)
meds = np.array(meds)
quantiles = np.array(quantiles)

mean_var = np.var(means, axis=0)
med_var = np.var(meds, axis=0)
quantile_var = np.var(quantiles, axis=0)

print('\n' + f'mean_var = {np.round(mean_var, 3)}, med_var = {np.round(med_var, 3)}')
print('\n'.join(f'quantile {q_values[i]} var = {quantile_var[i]}' for i in range(len(q_values))))


def draw_plots(means, meds, quantiles, title):
    _, ax = plt.subplots()

    x = [i for i in range(1, 11)]

    ax.plot(x, means, color='r', label='means')
    ax.plot(x, meds, color='b', label='medians')
    ax.plot(x, quantiles[:, 0], color='y', label='q_02')
    ax.plot(x, quantiles[:, 1], color='m', label='q_04')
    ax.plot(x, quantiles[:, 2], color='k', label='q_06')
    ax.plot(x, quantiles[:, 3], color='g', label='q_08')

    ax.legend(bbox_to_anchor=(1, 1))

    ax.set(xlabel='x', ylabel='y', title=title)
    ax.grid()
    plt.tight_layout()

    
draw_plots(means[:, 0], meds[:, 0], quantiles[:, :, 0], 'data1')
draw_plots(means[:, 1], meds[:, 1], quantiles[:, :, 1], 'data2')

plt.show()