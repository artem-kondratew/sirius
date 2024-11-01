import matplotlib.pyplot as plt
import sys
import numpy as np
# from legendre_approx import approx


if __name__ == '__main__':
    assert len(sys.argv) == 3

    with open(sys.argv[1], 'r') as file:
        lines = file.read().split('\n')
        data = []
        for line in lines:
            if line == '':
                continue
            data.append(list(float(s) for s in line.split(',')))

    data = np.array(data)
    x = data[:, 0]
    y = data[:, 1]

    with open(sys.argv[2], 'r') as file:
        lines = file.read().split('\n')
        data = []
        for line in lines:
            if line == '':
                continue
            data.append(list(float(s) for s in line.split(',')))

    data = np.array(data)
    y_approx = data[:, 1]

    fig, ax = plt.subplots()
    # ax.plot(x, y, color='r')
    ax.plot(x, y_approx, color='b')
    
    ax.legend('approx')

    ax.set(xlabel='x', ylabel='y',
       title='Legendre approx')
    ax.grid()

    # fig.savefig("test.png")
    plt.show()
