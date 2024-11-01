import sys
import numpy as np


if __name__ == '__main__':
    assert len(sys.argv) == 2

    with open(sys.argv[1], 'w') as file:
        a = -1
        b = 1
        s = 0.02
        x = np.arange(a, b + s, s)
        y = np.sin(x)
        for i, j in zip(x, y):
            file.write(f'{i},{j}\n')
