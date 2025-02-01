import matplotlib.pyplot as plt 
import numpy as np

x, t = [2, 0.5], 0 #Начальные значения
integral_part = 0

t1 = 30.0 #Период симуляции
dt = 0.0001 #Шаг по времени

solution = [] #Массивы для хранения значений
tarr = []
uarr = []
sigmaarr = []


def sign_exp(x, p):
    return np.sign(x) * np.abs(x) ** p


def rhs(t, state):
    global integral_part

    x1, x2 = state

    m = 4
    k = 1.5 + 0.4 * np.sin(2 * t)

    sigma = x2 + 0.5 * x1

    k1 = 10
    k2 = 1
    
    integral_part += np.sign(sigma) * dt
    u = -k1 * sign_exp(sigma, 0.5) - k2 * integral_part
    
    uarr.append(u)
    sigmaarr.append(sigma)

    dx1 = x2
    dx2 = (u - k * x2 * abs(x2)) / m
    
    return [dx1, dx2]

while t < t1:
    dx = rhs(t, x)
    x = [x[0]+dx[0]*dt, x[1]+dx[1]*dt] # Применяем метод Эйлера

    solution.append(x)
    tarr.append(t)
    t += dt

y1, y2 = zip(*solution)

fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(7,5), sharex=True) # Вывод графиков (добавить вывод u)

ax1.set_xlabel('Time, s')
ax1.set_ylabel('X1, X2')
ax1.plot(tarr, y2, 'b-')
ax1.plot(tarr, y1, 'r-')
ax1.grid(True)

ax2.set_xlabel('Time, s')
ax2.set_ylabel('sigma')
ax2.plot(tarr, sigmaarr, 'k-')
ax2.grid(True)

ax3.set_xlabel('Time, s')
ax3.set_ylabel('u')
ax3.plot(tarr, uarr, 'k-')
ax3.grid(True)

plt.show()