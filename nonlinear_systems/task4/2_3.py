import matplotlib.pyplot as plt 
import numpy as np


L = 20 * 10 ** -3
C = 20 * 10 ** -6
R = 30
Vin = 15
Vd = 10

x = [0.1, 5]

t = 0.0
t1 = 10
dt = 0.0001

tarr = []
xarr = []
uarr = []


def rhs(x):
    x1, x2 = x

    sigma = x1 - Vd / R
    u = 0.5 * (1 - np.sign(sigma))

    dx1 = 1 / L * (-x2 + Vin * u)
    dx2 = 1 / C * (x1 - x2 / R)

    uarr.append(u)

    return [dx1, dx2]


while t < t1:
    dx = rhs(x)
    x = [x[0]+dx[0]*dt, x[1]+dx[1]*dt]

    xarr.append(x)
    tarr.append(t)

    t += dt


x1, x2 = zip(*xarr)

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(7,5), sharex=True)

ax1.set_xlabel('Time, s')
ax1.set_ylabel('$i$, $v$')
ax1.plot(tarr, x1, 'b-', label='$i$')
ax1.plot(tarr, x2, 'r-', label='$v$')
ax1.legend(loc='upper right')
ax1.grid(True)

ax2.set_xlabel('Time, s')
ax2.set_ylabel('$u$')
ax2.plot(tarr, uarr, 'g-', label='$u$')
ax2.legend(loc='upper right')
ax2.grid(True)

plt.show()