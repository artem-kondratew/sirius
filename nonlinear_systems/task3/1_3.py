import matplotlib.pyplot as plt 
import numpy as np

x, t = [2, 0.5, 0, 1], 0 #Начальные значения
u = 0

t1 = 30.0 #Период симуляции
dt = 0.0001 #Шаг по времени

solution = [] #Массивы для хранения значений
tarr = []
uarr = []
sigmaarr = []
varr = []
dsigmaarr = []
sarr = []


def sign_exp(x, p):
    return np.sign(x) * np.abs(x) ** p


def observer(state):
    x1, x2, sigma1e, sigma2e = state
    sigma1 = x1 + x2

    k1 = 15
    k2 = 11

    dsigma1e = -k1 * sign_exp(sigma1e - sigma1, 0.5) + sigma2e
    dsigma2e = -k2 * np.sign(sigma1e - sigma1)

    return [dsigma1e, dsigma2e]


def rhs(t, state): # Функция возвращает правые части уравнений
    global u

    x1, x2, _, sigma2e = state

    m = 4
    k = 1.5 + 0.4 * np.sin(2 * t)

    sigma = x2 + x1

    dsigma = sigma2e
    
    s = dsigma + sigma
    v = -10 * np.sign(s)
    u += v * dt
    
    uarr.append(u)
    varr.append(v)
    sarr.append(s)
    dsigmaarr.append(dsigma)
    sigmaarr.append(sigma)

    dx1 = x2
    dx2 = (u - k * x2 * np.abs(x2)) / m
    
    return [dx1, dx2]


while t < t1:
    dsigmae = observer(x)
    dx = rhs(t, x)

    x[2] = x[2] + dsigmae[0] * dt
    x[3] = x[3] + dsigmae[1] * dt

    x[0] = x[0] + dx[0] * dt
    x[1] = x[1] + dx[1] * dt

    solution.append(x[:2])
    tarr.append(t)
    t += dt


y1, y2 = zip(*solution)

import matplotlib.pyplot as plt

import matplotlib.pyplot as plt

fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(7, 5), sharex=True)

# Первый график: x1, x2
ax1.set_xlabel('Time, s')
ax1.set_ylabel('$x_1$, $x_2$')
ax1.plot(tarr, y2, 'b-', label='$x_2$')
ax1.plot(tarr, y1, 'r-', label='$x_1$')
ax1.legend(loc='upper right', bbox_to_anchor=(1, 1))
ax1.grid(True)

# Второй график: s, sigma, sigma_dot
ax2.set_xlabel('Time, s')
ax2.set_ylabel('$s$, $\\sigma$, $\\dot{\\sigma}$')
ax2.plot(tarr, sigmaarr, 'b-', label='$\\sigma$')
ax2.plot(tarr, dsigmaarr, 'r-', label='$\\dot{\\sigma}$')
ax2.plot(tarr, sarr, 'g-', label='$s$')
ax2.legend(loc='upper right', bbox_to_anchor=(1, 1))
ax2.grid(True)

# Третий график: v, u
ax3.set_xlabel('Time, s')
ax3.set_ylabel('$v$, $u$')
ax3.plot(tarr, varr, 'b-', label='$v$')
ax3.plot(tarr, uarr, 'r-', label='$u$')
ax3.legend(loc='upper right', bbox_to_anchor=(1, 1))
ax3.grid(True)

plt.tight_layout()  # Улучшает расположение графиков
plt.show()

