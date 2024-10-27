import numpy as np
import scipy.stats as stats
import math
import matplotlib.pyplot as plt


VARIANT = 5
confidence_levels = [0.95, 0.99]

with open('./data1905.csv', 'r') as file:
    lines = file.read().split('\n')
    data = [[], [], []]
    for line in lines:
        if line == '':
            continue
        line = line.split(',')
        v = int(line[0])
        name = line[1].strip('"')
        r = float(line[2])
        data[0].append(v)
        data[1].append(name)
        data[2].append(r)
        
variants = np.array(data[0])
names = np.array(data[1])[variants == VARIANT]
rs = np.array(data[2])[variants == VARIANT]

planets = dict()

for r, name in zip(rs, names):
    if not name in planets:
        planets[name] = []
    planets[name].append(r)
    
for planet, values in planets.items():
    mean = np.mean(values)
    var = np.var(values, ddof=1)
    std = np.std(values, ddof=1)
    n = len(values)
    
    intervals = dict()
    for confidence_level in confidence_levels:
        q_central = (1 + confidence_level) / 2
        t_central = stats.t.ppf(q_central, df=n - 1)
        
        central_lower_bound = mean - t_central * std / math.sqrt(n)
        central_upper_bound = mean + t_central * std / math.sqrt(n)
        
        q_right = confidence_level
        t_right = stats.t.ppf(q_right, df=n - 1)
        
        right_bound = mean - t_right * std / math.sqrt(n)
        
        intervals[confidence_level] = {
                'central_lower' : central_lower_bound,
                'central_upper' : central_upper_bound,
                'right' : right_bound,
                }
        
    var_intervals = dict()
    for confidence_level in confidence_levels:
        alpha = 1.0 - confidence_level
        
        chi2_central_lower = stats.chi2.ppf(1 - alpha / 2, n - 1)
        chi2_central_upper = stats.chi2.ppf(alpha / 2, n - 1)
        chi2_left = stats.chi2.ppf(alpha, n - 1)
        
        central_lower_bound = (n - 1) * var / chi2_central_lower
        central_upper_bound = (n - 1) * var / chi2_central_upper
        left_bound = (n - 1) * var / chi2_left
        
        var_intervals[confidence_level] = {
                'central_lower' : central_lower_bound,
                'central_upper' : central_upper_bound,
                'left' : left_bound,
                }
        
    SEP = std * math.sqrt(1 + 1 / n)    
        
    confidence_level = confidence_levels[0] # 0.95

    c = stats.t.ppf((1 + confidence_level) / 2, n - 1)

    lower_bound = mean - c * SEP
    upper_bound = mean + c * SEP

    prediction_interval = {
        'lower' : lower_bound,
        'upper' : upper_bound,
        }
    
    planets[planet] = {
        'mean' : mean,
        'var' : var,
        'std' : std,
        # 'values' : np.array(values),
        'n' : n,
        'intervals' : intervals,
        'var_intervals' : var_intervals,
        'prediction_interval' : prediction_interval,
    }   


Earth = planets['Earth']
print(Earth)

# mean = Earth['mean']
# var = Earth['var']
# std = Earth['std']

# x = np.linspace(mean - 4 * std, mean + 4 * std, 100)
# y = stats.norm.pdf(x, mean, std)

# fig, ax = plt.subplots()

# ax.plot(x, y, label='Нормальное распределение', color='blue')
# ax.scatter(Earth['values'], stats.norm.pdf(Earth['values'], mean, std), color='red', marker='o', label='Значения выборки', zorder=5)

# plt.axvline(Earth['mean'], color='green', linestyle='--', label='Матожидание')

# plt.axvline(Earth['intervals'][0.95]['central_lower'], color='red', linestyle='--', label=f'Центр. дов. интервал 95%')
# plt.axvline(Earth['intervals'][0.95]['central_upper'], color='red', linestyle='--')

# plt.axvline(Earth['intervals'][0.99]['central_lower'], color='magenta', linestyle='--', label=f'Центр. дов. интервал 99%')
# plt.axvline(Earth['intervals'][0.99]['central_upper'], color='magenta', linestyle='--')

# plt.axvline(Earth['intervals'][0.95]['right'], color='black', linestyle='-.', label=f'Прав. интервал 95%')

# plt.axvline(Earth['intervals'][0.99]['right'], color='brown', linestyle='-.', label=f'Прав. интервал 99%')

# plt.legend(bbox_to_anchor=(1, 1))

# ax.set(xlabel='x', ylabel='y', title='Earth')
# plt.grid()
# plt.tight_layout()

# plt.show()
