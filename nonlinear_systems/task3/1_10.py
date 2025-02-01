import matplotlib.pyplot as plt 
import numpy as np


x, t = [1, 0, 1, 0, 0, 0, 0], 0
v = 0

t1 = 30.0
dt = 0.0001

solution = []
tarr = []
uarr = []
derx = []
trackerr = []
zerr = []
sigmaerr = []
phiarr = []
varr = []

J = 10 ** -3
R = 1
L = 0.5
km = kb = 5 * 10 ** -2


def sign_exp(x, p):
    return np.sign(x) * np.abs(x) ** p


def observer(state):
    x1, _, z1e, z2e, x_track, sigma1e, sigma2e = state
    z1 = x1 - x_track
    sigma1 = z2e + z1

    Lc = 0.1 / J

    k1 = 1.5 * np.sqrt(Lc) * 10
    k2 = 1.1 * Lc * 10

    dz1e = -k1 * sign_exp(z1e - z1, 0.5) + z2e 
    dz2e = -k2 * np.sign(z1e - z1)

    dsigma1e = -k1 * sign_exp(sigma1e - sigma1, 0.5) + sigma2e
    dsigma2e = -k2 * np.sign(sigma1e - sigma1)

    return [dz1e, dz2e], [dsigma1e, dsigma2e]


def rhs(t, state):
    global v

    x1, x2, _, z2e, x_track, sigma1e, sigma2e = state

    TL = 0.1 * np.sin(t)

    z1 = x1 - x_track

    sigma = z2e + z1
    s = sigma2e + 24 * sigma

    sigmaerr.append(sigma - sigma1e)

    ro = 4

    phi = -ro * np.sign(s)
    v += phi * dt
    u = v + R * x2 + kb * x1
    
    uarr.append(u)
    phiarr.append(phi)
    varr.append(v)

    dx1 = 1 / J * (km * x2 - TL)
    dx2 = 1 / L * v
    
    return [dx1, dx2]


while t < t1:
    dze, dsigmae = observer(x)
    dx = rhs(t, x)

    x[4] = 0.2 * np.sin(2 * t)

    x[2] = x[2] + dze[0] * dt
    x[3] = x[3] + dze[1] * dt

    x[5] = x[5] + dsigmae[0] * dt
    x[6] = x[6] + dsigmae[1] * dt

    x[0] = x[0] + dx[0] * dt
    x[1] = x[1] + dx[1] * dt

    zerr.append(x[0] - x[2] - x[4])

    x_track = x[4]
    trackerr.append(x_track - x[0])

    derx.append(dx)
    solution.append(x[:2])
    tarr.append(t)
    t += dt


y1, y2 = zip(*solution)
dy1, dy2 = zip(*derx)


fig, (ax1, ax2, ax3, ax4, ax5) = plt.subplots(5, 1, figsize=(7,7), sharex=True)

plt.subplots_adjust(hspace=0.5)

ax1.set_xlabel('Time, s')
ax1.set_ylabel('$x_1$, $x_2$')
ax1.plot(tarr, y2, 'b-', label='$x_2$')
ax1.plot(tarr, y1, 'r-', label='$x_1$')
ax1.legend(loc='upper right')
ax1.grid(True)

ax2.set_xlabel('Time, s')
ax2.set_ylabel('Tracking error')
ax2.plot(tarr, trackerr, 'b-')
ax2.grid(True)

ax3.set_xlabel('Time, s')
ax3.set_ylabel('$z_{err}$')
ax3.plot(tarr, zerr, 'g-')
ax3.grid(True)

ax4.set_xlabel('Time, s')
ax4.set_ylabel('$\sigma_{err}$')
ax4.plot(tarr, sigmaerr, 'm-')
ax4.grid(True)

ax5.set_xlabel('Time, s')
ax5.set_ylabel('$u$, $v$, $\phi$')
ax5.plot(tarr, varr, 'b-', label='$v$')
ax5.plot(tarr, uarr, 'r-', label='$u$')
ax5.plot(tarr, phiarr, 'g-', label='$\phi$')
ax5.legend(loc='upper right')
ax5.grid(True)

plt.subplots_adjust(hspace=0.5)
plt.show()
