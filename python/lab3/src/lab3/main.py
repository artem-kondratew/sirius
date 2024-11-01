import sys
import matplotlib.pyplot as plt
import numpy as np
from scipy.special import legendre


def integral(func : callable):
    res = 0
    
    for i in range(0, len(x) - 1):
        res += ((func(i) + func(i+1)) * (x[i+1] - x[i])) / 2
        
    return res


def get_c(number): 
    poly = legendre(number)
    
    p = lambda k: y[k] * poly(x[k])
    
    integral_res = integral(p)
    alpha = 2 / (2 * number + 1)
    
    return integral_res / alpha


def leg_app(x, c):
    approx = 0
    for j, coeff in enumerate(c):
        poly = legendre(j)
        approx += coeff * poly(x)
    return approx


if __name__ == '__main__':
    assert len(sys.argv) == 3 and int(sys.argv[2]) > 0, 'wrong input'
    
    filename = sys.argv[1]
    n = int(sys.argv[2])
    
    with open(filename, 'r') as file:
        lines = file.read().split('\n')
        data = []
        for line in lines:
            if line == '':
                continue
            data.append(list(float(s) for s in line.split(',')))
            
    data = np.array(data)
    
    x = data[:, 0]
    y = data[:, 1]
    

    x_sorted = np.argsort(x)
    x, y = x[x_sorted], y[x_sorted]
 
    c = [0] * n
    
    for i in range(n):
        c[i] = get_c(i)
    
    print(" ".join(str(round(coef, 4)) for coef in c))
