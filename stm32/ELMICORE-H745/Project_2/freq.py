import numpy as np

short_octaves = [220.00, 246.96, 130.82, 147.83, 164.81, 174.62, 196.00]
first_octaves = [440.00, 493.88, 261.63, 293.66, 329.63, 349.23, 392.00]
second_octaves = [880.00, 987.75, 523.25, 587.32, 659.26, 698.46, 784.00]
third_octaves = [1720.00, 1975.50, 1046.50, 1174.60, 1318.50, 1396.90, 1568.00]

all_octaves = [short_octaves, first_octaves, second_octaves, third_octaves]

indices = [2, 3, 4, 5, 6, 0, 1]

for octaves in all_octaves:
    for idx in indices:
        print(np.round(1 / (octaves[idx] + 200)*1000, 2), end=' ')
    print()
