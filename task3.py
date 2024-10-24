import numpy as np
import scipy.stats as stats
import math
import matplotlib.pyplot as plt


with open('./data0505.csv', 'r') as file:
    lines = file.read().split('\n')
    data = []
    for line in lines:
        if line == '':
            continue
        data.append(list(s for s in line.split(',')))

languages = dict()

for d in data:
    lang = d[0].strip('"')
    val = float(d[1])
    
    if not lang in languages:
        languages[lang] = []
    
    languages[lang].append(val)

levels = [0.90, 0.95, 0.99]

for lang in languages.keys():
    values = languages[lang]
    mean = np.mean(values)
    std = np.std(values)
    n = len(values)
    df = n - 1
    
    intervals = dict()
    for level in levels:
        
        t_left = stats.t.ppf(level, df)
        t_central = stats.t.ppf(1 - (1 - level) / 2, df)
    
        left_bound = mean + t_left * std / math.sqrt(df)
        central_lower_bound = mean - t_central * std / math.sqrt(df)
        central_upper_bound = mean + t_central * std / math.sqrt(df)
        
        intervals[level] = {
            'left' : left_bound,
            'central_lower' : central_lower_bound,
            'central_upper' : central_upper_bound,
            }
    
    languages[lang] = {
        'mean' : mean,
        'std' : std,
        'n' : n,
        'intervals' : intervals,
        'values' : languages[lang],
        }

cnt = {level : {'left' : 0, 'central' : 0} for level in levels}
mu = 100.0

for lang in languages.keys():
    lang = languages[lang]
    for level in levels:
        left = lang['intervals'][level]['left']
        central_lower = lang['intervals'][level]['central_lower']
        central_upper = lang['intervals'][level]['central_upper']
        if mu > left:
            cnt[level]['left'] += 1
        elif not central_lower <= mu <= central_upper:
            cnt[level]['central'] += 1

# print(cnt)
# print('(3, 8), (2, 4), (0, 1)')
N = len(languages.keys())
for level in levels:
    print(f'level = {level}:\n\tleft: {cnt[level]["left"]} ({100 * cnt[level]["left"] / N} %)' \
        f'\n\tcentral: {cnt[level]["central"]} ({100 * cnt[level]["central"] / N} %)')

theoretical_mu = [N * (1.0 - level) for level in levels]
print('\nEt =', theoretical_mu)

lang = languages['English']
# print(lang)

plt.plot(lang['values'], range(lang['n']), 'o', label='Observations', color='blue')
plt.axvline(lang['mean'], color='green', linestyle='--', label='Mean')

plt.axvline(lang['intervals'][0.90]['central_lower'], color='red', linestyle='--', label=f'Lower CI ({level*100}%)')
plt.axvline(lang['intervals'][0.90]['central_upper'], color='red', linestyle='--', label=f'Upper CI ({level*100}%)')

plt.axvline(lang['intervals'][0.95]['central_lower'], color='magenta', linestyle='--', label=f'Lower CI ({level*100}%)')
plt.axvline(lang['intervals'][0.95]['central_upper'], color='magenta', linestyle='--', label=f'Upper CI ({level*100}%)')

plt.axvline(lang['intervals'][0.99]['central_lower'], color='black', linestyle='--', label=f'Lower CI ({level*100}%)')
plt.axvline(lang['intervals'][0.99]['central_upper'], color='black', linestyle='--', label=f'Upper CI ({level*100}%)')

plt.show()
