import matplotlib.pyplot as plt 
import numpy as np


J1 = 1
J2 = 0.8
J3 = 0.4

t1 = 30.0
dt = 0.0001

B = np.diag([1 / J1, 1 / J2, 1 / J3])

G = np.linalg.inv(B)

x0 = np.array([[0.5, -1, 2]]).T
x = x0
t = 0.0

integral_part = 0

tarr = []
xarr = []
uarr = []
sigmaarr = []


def rhs(x):
    global integral_part

    x1 = x[0][0]
    x2 = x[1][0]
    x3 = x[2][0]

    phi = np.array([[(J2 - J3) * x2 * x3],
                    [(J3 - J1) * x3 * x1],
                    [(J1 - J2) * x1 * x2]])
    
    # phi = np.zeros((3, 1))
    
    u0 = -np.eye(3) @ x

    alpha = 1
    integral_part = integral_part + B @ u0 * dt
    sigma = G @ (x - x0) - G @ integral_part
    u1 = -alpha * np.sign(sigma)

    u = u0 + u1

    dx = B @ (u + phi)

    uarr.append(u)
    sigmaarr.append(sigma)

    return dx

while t < t1:
    dx = rhs(x)
    x = x + dx * dt

    xarr.append(x)

    tarr.append(t)
    t += dt

xarr = np.array(xarr)
uarr = np.array(uarr)
sigmaarr = np.array(sigmaarr)

fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(7,5), sharex=True)

ax1.set_xlabel('Time, s')
ax1.set_ylabel('$x_1$, $x_2$, $x_3$')
ax1.plot(tarr, xarr[:, 0, 0].flatten(), 'b-', label='$x_1$')
ax1.plot(tarr, xarr[:, 1, 0].flatten(), 'r-', label='$x_2$')
ax1.plot(tarr, xarr[:, 2, 0].flatten(), 'g-', label='$x_3$')
ax1.legend(loc='upper right')
ax1.grid(True)

ax2.set_xlabel('Time, s')
ax2.set_ylabel('$u$')
ax2.plot(tarr, uarr[:, 2, 0].flatten(), 'g-', label='$u_3$')
ax2.plot(tarr, uarr[:, 0, 0].flatten(), 'b-', label='$u_1$')
ax2.plot(tarr, uarr[:, 1, 0].flatten(), 'r-', label='$u_2$')
ax2.legend(loc='upper right')
ax2.grid(True)

ax3.set_xlabel('Time, s')
ax3.set_ylabel('$\\sigma$')
ax3.plot(tarr, sigmaarr[:, 0, 0].flatten(), 'b-', label='$\\sigma_1$')
ax3.plot(tarr, sigmaarr[:, 1, 0].flatten(), 'r-', label='$\\sigma_2$')
ax3.plot(tarr, sigmaarr[:, 2, 0].flatten(), 'g-', label='$\\sigma_3$')
ax3.legend(loc='upper right')
ax3.grid(True)

plt.show()