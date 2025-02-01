import matplotlib.pyplot as plt 
import numpy as np


A = np.array([[2, 19],
              [3, 29]])

B = np.array([[2, 3]]).T

G = np.array([[9, 12]])

t1 = 30.0
dt = 0.0001

x = np.array([[-2, -2]]).T
t = 0

tarr = []
xarr = []
uarr = []
sigmaarr = []

I = np.eye(2)
M = (I - B @ np.linalg.inv(G @ B) @ G) @ A

print(M)
print(np.linalg.eigvals(M))


def rhs(x):
    sigma = G @ x
    sigma = sigma[0][0]

    x1 = x[0, 0]
    x2 = x[1, 0]

    u = -x1 - 519 / 54 * x2 - np.sign(sigma)

    dx = A @ x + B * u

    sigmaarr.append(sigma)
    uarr.append(u)
    xarr.append(x)

    return dx


while t < t1:
    dx = rhs(x)
    x = x + dx * dt

    tarr.append(t)
    t += dt

xarr = np.array(xarr)

fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(7,5), sharex=True)

ax1.set_xlabel('Time, s')
ax1.set_ylabel('$x_1$, $x_2$')
ax1.plot(tarr, xarr[:, 0, 0].flatten(), 'b-', label='$x_1$')
ax1.plot(tarr, xarr[:, 1, 0].flatten(), 'r-', label='$x_2$')
ax1.legend(loc='upper right')
ax1.grid(True)

ax2.set_xlabel('Time, s')
ax2.set_ylabel('$u$')
ax2.plot(tarr, uarr, 'b-', label='$u$')
ax2.legend(loc='upper right')
ax2.grid(True)

ax3.set_xlabel('Time, s')
ax3.set_ylabel('$\\sigma$')
ax3.plot(tarr, sigmaarr, 'b-', label='$\\sigma$')
ax3.legend(loc='upper right')
ax3.grid(True)

plt.show()