import matplotlib.pyplot as plt 
import numpy as np

x, t = [2, 0.5], 0 #Начальные значения

t1 = 30.0 #Период симуляции
dt = 0.0001 #Шаг по времени

solution = [] #Массивы для хранения значений
tarr = []
uarr = []
z2list = []
derx = []
sigmaarr = []


def rhs(t, state): # Функция возвращает правые части уравнений

    x1, x2 = state

    m = 4
    k = 1.5 + 0.4 * np.sin(2 * t)

    sigma = x2 + x1

    print(sigma)

    e = 0.1 
    km = 1.9 
    ro = km * x2 * x2 + 1
    u = -ro * sigma / (np.abs(sigma) + e) - m * x2
    
    uarr.append(u)
    sigmaarr.append(sigma)

    dx1 = x2
    dx2 = (u - k * x2 * abs(x2)) / m
    
    return [dx1, dx2]

while t < t1:
    dx = rhs(t, x)

    x = [x[0] + dx[0] * dt, x[1] + dx[1] * dt]

    derx.append(dx)
    solution.append(x)
    tarr.append(t)
    t += dt

y1, y2 = zip(*solution)
dy1, dy2 = zip(*derx)

fig, (ax1, ax2, ax3, ax4) = plt.subplots(4, 1, figsize=(7,5), sharex=True) # Вывод графиков (добавить вывод u)
ax1.set_xlabel('Time, s')
ax1.set_ylabel('X1')
ax1.plot(tarr, y1, 'k-')
ax1.grid(True)

ax2.set_xlabel('Time, s')
ax2.set_ylabel('X2')
ax2.plot(tarr, y2, 'k-')
ax2.grid(True)

ax3.set_xlabel('Time, s')
ax3.set_ylabel('X1, X2')
ax3.plot(tarr, y2, 'b-')
ax3.plot(tarr, y1, 'r-')
ax3.grid(True)

ax4.set_xlabel('Time, s')
ax4.set_ylabel('sigma')
ax4.plot(tarr, sigmaarr, 'b-')
ax4.grid(True)

fi2, (ax21, ax22, ax23) = plt.subplots(3, 1, figsize=(7,5), sharex=True)
ax21.set_xlabel('Time, s')
ax21.set_ylabel('dX1')
ax21.plot(tarr, dy1, 'k-')
ax21.grid(True)

ax22.set_xlabel('Time, s')
ax22.set_ylabel('dX2')
ax22.plot(tarr, dy2, 'k-')
ax22.grid(True)

ax23.set_xlabel('Time, s')
ax23.set_ylabel('u')
ax23.plot(tarr, uarr, 'k-')
ax23.grid(True)

plt.show()