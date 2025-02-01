import matplotlib.pyplot as plt 
import numpy as np


x, t = [1, 0, 1, 0, 0, 0, 0, 0], 0  # Начальные значения

t1 = 30.0  # Период симуляции
dt = 0.0001  # Шаг по времени

solution = []  # Массивы для хранения значений
tarr = []
uarr = []
sarr  = []
varr = []
x1earr = []

J = 10 ** -3
R = 1
L = 0.5
km = kb = 5 * 10 ** -2


def sign_exp(x, p):
    return np.sign(x) * np.abs(x) ** p


def observer(state):
    _, x2, z1e, z2e, _, x2e, ddx2e, u = state

    Lc = 0.1 / J

    k1 = 15
    k2 = 20

    dx2e = -k1 * sign_exp(x2e - x2, 0.5) + ddx2e
    ddx2e = -k2 * np.sign(x2e - x2)

    x1e = 1 / kb * (-L * dx2e - R * x2 + u)

    z1 = x1e

    Lc = 0.1 / J

    k1 = 1.5 * np.sqrt(Lc)
    k2 = 1.1 * Lc

    dz1e = -k1 * sign_exp(z1e - z1, 0.5) + z2e
    dz2e = -k2 * np.sign(z1e - z1)

    return [dz1e, dz2e], x1e, x2e, ddx2e


def rhs(t, state):

    _, x2, _, z2e, x1e, _, _, _ = state

    TL = 0.1 * np.sin(t)

    TL_dot_max = 0.1
    alpha = TL_dot_max * L / km
    beta = 1

    s = z2e + beta * sign_exp(x1e, 0.5)
    v = -alpha * np.sign(s)
    u = v + R * x2 + kb * x1e
    
    uarr.append(u)
    varr.append(v)
    sarr.append(s)

    dx1 = 1 / J * (km * x2 - TL)
    dx2 = 1 / L * v
    
    return [dx1, dx2], u


while t < t1:
    dze, x1e, x2e, ddx2e = observer(x)
    dx, u = rhs(t, x)

    x[-1] = u
    x[-2] = ddx2e
    x[-3] = x2e
    x[-4] = x1e

    x[2] = x[2] + dze[0] * dt
    x[3] = x[3] + dze[1] * dt

    x[0] = x[0] + dx[0] * dt
    x[1] = x[1] + dx[1] * dt

    solution.append(x[:2])
    tarr.append(t)
    x1earr.append(x1e)
    t += dt


y1, y2 = zip(*solution)


fig, (ax1, ax2, ax3, ax4) = plt.subplots(4, 1, figsize=(7, 5), sharex=True)

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

ax4.set_xlabel('Time, s')
ax4.set_ylabel('$x_1$, $x_1$ est.')
ax4.plot(tarr, y1, 'r-', label='$x_1$')
ax4.plot(tarr, x1earr, 'b-', label='$x_1$ est.')
ax4.legend(loc='upper right')
ax4.grid(True)

plt.tight_layout()  # Улучшает размещение графиков
plt.show()
