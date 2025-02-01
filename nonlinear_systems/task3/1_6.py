import matplotlib.pyplot as plt 
import numpy as np


x, t = [1, 0, 1, 0], 0  # Начальные значения

t1 = 30.0  # Период симуляции
dt = 0.0001  # Шаг по времени

solution = []  # Массивы для хранения значений
tarr = []
uarr = []
sarr  = []
varr = []

J = 10 ** -3
R = 1
L = 0.5
km = kb = 5 * 10 ** -2


def sign_exp(x, p):
    return np.sign(x) * np.abs(x) ** p


def observer(state):
    x1, _, z1e, z2e = state
    z1 = x1

    Lc = 0.1 / J

    k1 = 1.5 * np.sqrt(Lc)
    k2 = 1.1 * Lc

    dz1e = -k1 * sign_exp(z1e - z1, 0.5) + z2e
    dz2e = -k2 * np.sign(z1e - z1)

    return [dz1e, dz2e]


def rhs(t, state):

    x1, x2, _, z2e = state

    TL = 0.1 * np.sin(t)

    TL_dot_max = 0.1
    alpha = TL_dot_max * L / km
    beta = 1

    s = z2e + beta * sign_exp(x1, 0.5)
    v = -alpha * np.sign(s)
    u = v + R * x2 + kb * x1
    
    uarr.append(u)
    varr.append(v)
    sarr.append(s)

    dx1 = 1 / J * (km * x2 - TL)
    dx2 = 1 / L * v
    
    return [dx1, dx2]


while t < t1:
    dze = observer(x)
    dx = rhs(t, x)

    x[2] = x[2] + dze[0] * dt
    x[3] = x[3] + dze[1] * dt

    x[0] = x[0] + dx[0] * dt
    x[1] = x[1] + dx[1] * dt

    solution.append(x[:2])
    tarr.append(t)
    t += dt


y1, y2 = zip(*solution)


import matplotlib.pyplot as plt

fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(7, 5), sharex=True)

# Первый график: X1, X2
ax1.set_xlabel('Time, s')
ax1.set_ylabel('$x_1$, $x_2$')
ax1.plot(tarr, y2, 'b-', label='$x_2$')
ax1.plot(tarr, y1, 'r-', label='$x_1$')
ax1.legend(loc='upper right')
ax1.grid(True)

# Второй график: s
ax2.set_xlabel('Time, s')
ax2.set_ylabel('$s$')
ax2.plot(tarr, sarr, 'b-', label='$s$')
ax2.legend(loc='upper right')
ax2.grid(True)

# Третий график: u
ax3.set_xlabel('Time, s')
ax3.set_ylabel('$u$, $v$')
ax3.plot(tarr, varr, 'b-', label='$v$')
ax3.plot(tarr, uarr, 'r-', label='$u$')
ax3.legend(loc='upper right')
ax3.grid(True)

plt.tight_layout()  # Улучшает размещение графиков
plt.show()
