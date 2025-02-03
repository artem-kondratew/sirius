import matplotlib.pyplot as plt 
import numpy as np
from project_params import *


nu = 0


def sign_exp(x, p):
    return np.sign(x) * np.abs(x) ** p


def rhs(t, x):
    global nu

    phi = -m * np.sin(t / d) + 0.1 * d * np.cos(30 * m * t)

    A = np.array([[0, 1, 0, 0],
                   [a21, a22, a23, 0],
                   [0, 0, 0, 1],
                   [a41, 0, a43, a44]])

    B = np.array([[0, b, 0, 0]]).T

    F = np.array([[a41 * (a21 + a43 + a44 ** 2)],
                  [a41 * (a22 + a44)],
                  [a23 * a41 + a43 ** 2 + a43 * a44 ** 2],
                  [a44 * (2 * a43 + a44 ** 2)]]).T

    y1 = x[2, 0]  # x3
    y2 = x[3, 0]  # x4
    y3 = np.array([[a41, 0, a43, a44]]) @ x  # x4_dot
    y4 = np.array([[a41 * a44, a41, a43 * a44, a43 + a44 ** 2]]) @ x  # x4_dot_dot

    c1 = 11
    c2 = 19
    c3 = 9
    psi1 = y4 + c1 * y3 + c2 * y2 + c3 * y1

    continuous_controller = False

    if continuous_controller:
        nu += -1.1 * Lc * sign_exp(psi1, 0) * dt
        theta1 = -1.5 * Lc ** (1/2) * sign_exp(psi1, 1/2) + nu
    else:
        theta1 = -1.1 * Ld * sign_exp(psi1, 0)  

    v1 = theta1 - (c1 * y4 + c2 * y3 + c3 * y3) / a41 / b

    u = v1 - F @ x / b / a41

    dx = A @ x + B * (u + phi)

    return dx, u[0][0], phi


def main():
    x, t = np.array([[1, 0, 1, 0]]).T, 0

    xarr = []
    tarr = []
    uarr = []
    phiarr = []

    while t < t1:
        dx, u, phi = rhs(t, x)
        x = x + dx * dt

        xarr.append(x)
        tarr.append(t)
        uarr.append(u)
        phiarr.append(phi)

        t += dt

    return xarr, tarr, uarr, phiarr


if __name__ == '__main__':
    xarr, tarr, uarr, phiarr = main()

    xarr= np.array(xarr)
    tarr = np.array(tarr)

    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(7, 5), sharex=True)

    ax1.set_xlabel('Time, s')
    ax1.set_ylabel('$x_1$, $x_2$, $x_3$, $x_4$')
    ax1.plot(tarr, xarr[:, 0, [0]].flatten(), 'b-', label='$x_1$')
    ax1.plot(tarr, xarr[:, 1, [0]].flatten(), 'r-', label='$x_2$')
    ax1.plot(tarr, xarr[:, 2, [0]].flatten(), 'g-', label='$x_3$')
    ax1.plot(tarr, xarr[:, 3, [0]].flatten(), 'y-', label='$x_4$')
    ax1.legend(loc='upper right')
    ax1.grid(True)

    ax2.set_xlabel('Time, s')
    ax2.set_ylabel('$u$')
    ax2.plot(tarr, uarr, 'b-', label='$u$')
    ax2.legend(loc='upper right')
    ax2.grid(True)

    ax3.set_xlabel('Time, s')
    ax3.set_ylabel('$phi$')
    ax3.plot(tarr, phiarr, 'b-', label='$phi$')
    ax3.legend(loc='upper right')
    ax3.grid(True)

    plt.tight_layout()
    plt.show()
